"""Deterministic intent preview. Never imports a CAD/CAE execution adapter."""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

REPO = Path(__file__).resolve().parents[1]
TABLE = 'simulation/cases/bga-2024r2-unsolved/data/geometry-parameters.csv'
CASE = 'bga-2024r2-unsolved'
NUMBER = r'[+-]?(?:\d+(?:\.\d+)?|\.\d+)'
ACTION = re.compile(r'调整为|改成|设为|改为|改小|减小|减薄|缩短|增大|加厚|加长|增加|减少|加|减')
NEGATIVE = re.compile(r'不要|不能|禁止|不许|别|无需|不用|不改|不修改|不变|不同步|不随动|不跟着变')
FOLLOW = re.compile(r'跟着变|一起变|同步|随之')
VALUE = re.compile(r'^\s*(' + NUMBER + r')\s*(毫米|微米|mm|[µμu]m|deg|度|°)?', re.I)


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise ValueError('Missing or duplicate CSV columns: ' + str(path))
        result = []
        for row in reader:
            if None in row or any(v is None for v in row.values()):
                raise ValueError('Malformed CSV row: ' + str(path))
            result.append({k: v.strip() for k, v in row.items()})
        return result


def unique(rows, key, label):
    result = {}
    for row in rows:
        name = row.get(key)
        if not name or name in result:
            raise ValueError(f'{label}: missing or duplicate {key}: {name}')
        result[name] = row
    return result


def decimal(text):
    try:
        value = Decimal(text)
    except InvalidOperation as error:
        raise ValueError('Invalid decimal value') from error
    if not value.is_finite():
        raise ValueError('Nonfinite value')
    return value


class Parser:
    def __init__(self, repo=REPO):
        self.repo = Path(repo)
        paths = [TABLE, 'shared/entities/registry.csv', 'tooling/nl_aliases.csv',
                 'tooling/nl_entity_map.csv', 'shared/tools/tools.schema.json']
        self.hashes = {path: hashlib.sha256((self.repo/path).read_bytes()).hexdigest()
                       for path in paths}
        self.parameters = unique(read_csv(self.repo/TABLE), 'logical_name', 'parameter table')
        self.entities = unique(read_csv(self.repo/paths[1]), 'stable_id', 'registry')
        self.aliases = unique(read_csv(self.repo/paths[2]), 'alias', 'aliases')
        self.mapping = {}
        for row in read_csv(self.repo/paths[3]):
            key = (row['case_id'], row['part_file'].casefold())
            if key in self.mapping:
                raise ValueError('Duplicate part/entity mapping')
            entity = self.entities.get(row['stable_id'])
            if not entity or entity['case_id'] != row['case_id'] or entity['entity_kind'] != 'body':
                raise ValueError('Entity mapping does not match the registry')
            self.mapping[key] = entity
        for row in self.aliases.values():
            parameter = self.parameters.get(row['logical_name'])
            if not parameter or parameter['part_file'].casefold() != row['part_file'].casefold():
                raise ValueError('Alias does not match parameter table')
        self.schema = json.loads((self.repo/paths[4]).read_text(encoding='utf-8-sig'))

    def match(self, subject):
        matches = []
        for alias, row in self.aliases.items():
            if alias in subject:
                matches.append((alias, row['logical_name']))
        # A short alias wholly contained in a longer match is the same mention.
        matches = [(a, n) for a, n in matches
                   if not any(a != b and a in b for b, _ in matches)]
        matches += [(name, name) for name in self.parameters
                    if re.search(r'(?<![A-Za-z0-9_])' + re.escape(name) + r'(?![A-Za-z0-9_])', subject)]
        names = sorted({n for _, n in matches})
        if names:
            return names
        parts = {'芯片': 'XINPIAN.SLDPRT', '塑封': 'SUFENGLIAO.SLDPRT',
                 '基板': 'JIBAN.SLDPRT', '底填': 'Underfill.SLDPRT',
                 '凸点': 'TUDIAN.SLDPRT', '焊球': 'HANQIU.SLDPRT'}
        mentioned = [file for label, file in parts.items() if label in subject]
        # Only a bare part or generic thickness is an ambiguous candidate set.
        if mentioned and any(word in subject for word in ['高度', '直径', '厚度', '长度', '宽度']):
            return []
        if mentioned:
            return sorted(n for n, row in self.parameters.items() if row['part_file'] in mentioned)
        if '厚度' in subject:
            return sorted(n for n in self.parameters if n.endswith('_thickness'))
        return []

    def parse(self, sentence):
        if not isinstance(sentence, str) or not sentence.strip():
            raise ValueError('Empty input')
        # Hash the exact sentence, including spaces. --stdin removes one final newline only.
        rid = 'nlr-' + hashlib.sha1(sentence.encode('utf-8')).hexdigest()[:12]
        text = unicodedata.normalize('NFKC', sentence)
        report = {'nl_schema_version': '0.1.0', 'case_id': CASE, 'request_id': rid, 'status': 'blocked',
                  'intents': [], 'contract_requests': [], 'unresolved': [], 'assumptions': [],
                  'data_sha256': self.hashes}
        report['input_fingerprint'] = hashlib.sha256(json.dumps(
            {'sentence': sentence, 'data': self.hashes,
             'parser_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
            ensure_ascii=False, sort_keys=True).encode('utf-8')).hexdigest()
        pending = []
        follow_primary = None
        for clause in re.split(r'[，,；;。\n]+', text):
            clause = clause.strip()
            if not clause:
                continue
            if NEGATIVE.search(clause):
                follow_primary = None
                report['unresolved'].append('U-NEGATION: ' + clause)
                continue
            follow = FOLLOW.search(clause)
            action = ACTION.search(clause)
            if follow and not action:
                if follow_primary is not None:
                    if follow_primary['follow_clause']:
                        report['unresolved'].append('U-CONFLICT: 多个随动描述需要明确作用对象')
                    else:
                        follow_primary['follow_clause'] = clause
                else:
                    report['unresolved'].append('U-FOLLOWER-WITHOUT-PRIMARY: ' + clause)
                continue
            follow_primary = None
            if not action:
                report['unresolved'].append('U-OPERATION-UNKNOWN: ' + clause)
                continue
            subject = clause[:action.start()]
            candidates = self.match(subject)
            if len(candidates) != 1:
                code = 'U-PARAM-AMBIGUOUS' if candidates else 'U-PARAM-UNKNOWN'
                report['unresolved'].append(code + ': ' + subject)
                continue
            name = candidates[0]
            value_match = VALUE.match(clause[action.end():])
            if not value_match:
                report['unresolved'].append('U-VALUE-UNKNOWN: ' + clause)
                continue
            rest = clause[action.end():][value_match.end():].strip()
            if rest and not FOLLOW.fullmatch(rest):
                report['unresolved'].append('U-UNSUPPORTED-EXPRESSION: ' + rest)
                continue
            number, unit = value_match.groups()
            row = self.parameters[name]
            unit = (unit or '').lower()
            assumptions = []
            if not unit:
                unit = 'mm'
                assumptions.append('未写单位，按 mm')
            amount = decimal(number)
            if unit in ['um', 'µm', 'μm', '微米']:
                amount *= Decimal('0.001')
                unit = 'mm'
                assumptions.append('输入微米已精确换算为 mm（乘以 0.001）')
            unit = {'毫米': 'mm', '°': 'deg', '度': 'deg'}.get(unit, unit)
            if unit != row['unit']:
                raise ValueError(f'Unit mismatch: {name} requires {row["unit"]}, got {unit}')
            operation = action.group()
            relative = operation not in ['调整为', '改成', '设为', '改为']
            if relative and amount < 0:
                raise ValueError('Relative magnitude must not be negative')
            delta = -amount if operation in ['改小', '减小', '减薄', '缩短', '减少', '减'] else amount
            current = decimal(row['current_value']) if relative else None
            value = current + delta if relative else amount
            if value <= 0:
                raise ValueError(f'Geometry value must be positive: {name}')
            entity = self.mapping.get((CASE, row['part_file'].casefold()))
            intent = {'intent_id': f'{rid}-{len(pending)+1:02d}', 'parameter': name,
                      'entity': entity['stable_id'] if entity else None,
                      'model_revision': entity['model_revision'] if entity else None,
                      'entity_resolution_state': entity['resolution_state'] if entity else 'unresolved',
                      'operation': 'relative' if relative else 'absolute',
                      'value': {'number': float(value), 'unit': unit},
                      'followers': [], 'follower_previews': [],
                      'confidence': {'parameter': 1.0, 'value': 1.0, 'unit': 1.0 if value_match.group(2) else 0.7},
                      'assumptions': assumptions, 'unresolved': [], 'follow_clause': clause if follow else None}
            if relative:
                intent.update(delta=float(delta), base_value=float(current), base_source=TABLE)
                intent['assumptions'].append('相对操作基于 CSV 快照，不代表当前软件会话数值')
            if not entity:
                intent['unresolved'].append('U-ENTITY-UNRESOLVED: ' + row['part_file'])
            elif entity['resolution_state'] != 'resolved':
                intent['unresolved'].append('U-ENTITY-RUNTIME: 仅登记归档实体，未确认当前会话身份')
            if row['class'] != 'A' or '含义待确认' in row.get('notes', ''):
                intent['unresolved'].append('U-PARAM-SEMANTICS: 参数分类或物理含义需要人工确认')
            pending.append(intent)
            follow_primary = intent
        for intent in pending:
            row = self.parameters[intent['parameter']]
            follow_clause = intent.pop('follow_clause')
            if follow_clause:
                specs = row.get('followers')
                if not specs:
                    intent['unresolved'].append('U-FOLLOWERS-UNAVAILABLE: 参数表未登记随动关系')
                else:
                    description = FOLLOW.sub('', follow_clause)
                    inline_action = ACTION.search(description)
                    if inline_action:
                        description = description[inline_action.end():]
                        description = VALUE.sub('', description).strip()
                    requested = self.match(description)
                    if description.strip() and not requested:
                        intent['unresolved'].append('U-FOLLOWER-UNKNOWN: ' + description)
                    names = []
                    for spec in specs.split(';'):
                        name, factor = spec.strip().split(':')
                        if name not in self.parameters or name == intent['parameter'] or name in names:
                            raise ValueError('Invalid or cyclic follower declaration')
                        names.append(name)
                        follower = self.parameters[name]
                        if follower.get('followers'):
                            raise ValueError('Recursive followers require explicit review')
                        if follower['unit'] != row['unit']:
                            raise ValueError('Follower unit mismatch')
                        change = decimal(str(intent['value']['number'])) - decimal(row['current_value'])
                        target = decimal(follower['current_value']) + decimal(factor) * change
                        if target <= 0:
                            raise ValueError('Follower value must be positive')
                        intent['followers'].append(name)
                        intent['follower_previews'].append({'parameter': name, 'value': {'number': float(target), 'unit': follower['unit']}, 'base_source': TABLE})
                    if requested and not set(requested).intersection(names):
                        intent['unresolved'].append('U-FOLLOWER-MISMATCH: 随动描述与登记关系不一致')
            else:
                intent['assumptions'].append('未要求随动，不自动补偿')
            intent['unresolved'].append('U-CONTRACT-GEOMETRY: 0.1.0 不能表达带值的 SolidWorks 参数修改')
            report['intents'].append(intent)
            report['assumptions'].extend(intent['assumptions'])
            report['unresolved'].extend(intent['unresolved'])
        changes = [i['parameter'] for i in pending]
        for intent in pending:
            if changes.count(intent['parameter']) > 1 or set(intent['followers']).intersection(changes):
                report['unresolved'].append('U-CONFLICT: 重复目标或主参数与随动参数冲突')
        report['assumptions'] = list(dict.fromkeys(report['assumptions']))
        report['unresolved'] = list(dict.fromkeys(report['unresolved']))
        validate_report(report, self.schema)
        return report


def validate_report(report, schema):
    """Validate the intent envelope; validate any embedded contract request in full."""
    if (report.get('nl_schema_version') != '0.1.0' or report.get('status') != 'blocked'
            or report.get('case_id') != CASE):
        raise ValueError('Phase one must remain a blocked preview')
    if not re.fullmatch(r'nlr-[0-9a-f]{12}', report.get('request_id', '')):
        raise ValueError('Invalid request ID')
    for key in ['intents', 'contract_requests', 'unresolved', 'assumptions']:
        if not isinstance(report.get(key), list):
            raise ValueError('Invalid report list: ' + key)
    for intent in report['intents']:
        value = intent['value']
        if decimal(str(value['number'])) <= 0 or value['unit'] not in ['mm', 'deg']:
            raise ValueError('Invalid intent quantity')
        if any(not 0 <= score <= 1 for score in intent['confidence'].values()):
            raise ValueError('Confidence out of range')
        for field, score in intent['confidence'].items():
            if score < 0.7 and not any(field in u for u in intent['unresolved']):
                raise ValueError('Low confidence must be unresolved')
    if report['contract_requests']:
        try:
            from jsonschema import Draft202012Validator
        except ImportError as error:
            raise ValueError('jsonschema is required for contract validation; no subset fallback') from error
        validator = Draft202012Validator(schema)
        for request in report['contract_requests']:
            validator.validate(request)
        raise ValueError('Phase one has no approved SolidWorks contract adapter')


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('sentence', nargs='?')
    cli.add_argument('--stdin', action='store_true')
    cli.add_argument('--repo', type=Path, default=REPO)
    options = cli.parse_args(argv)
    try:
        if options.stdin == (options.sentence is not None):
            raise ValueError('Use either one sentence or --stdin')
        sentence = sys.stdin.read().removesuffix('\n').removesuffix('\r') if options.stdin else options.sentence
        print(json.dumps(Parser(options.repo).parse(sentence), ensure_ascii=False, allow_nan=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError) as error:
        print('Validation error: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
        sys.stdin.reconfigure(encoding='utf-8')
    raise SystemExit(main())
