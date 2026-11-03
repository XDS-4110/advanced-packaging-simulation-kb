# DSH 接入 MCP 服务器：配置与排错

> 记录把本地 MCP 服务器接入 DeepSeek Harness 时踩到的问题。以 desktop profile 为例。

## 配置位置

`%USERPROFILE%\.dsh\profiles\desktop\cordis.patch.yml`

这是 profile 的**补丁层**，在 bundle 之后应用；`cordis.yml` 由程序合成，不要直接改。

## 关键：新增插件必须用 insert 包裹

```yaml
- insert:
    - id: mcp-solidworks
      name: "@deepseek-ai/dsh-mcp-client"
      config:
        serverName: solidworks
        transport: stdio
        command: "D:/SWMCP/.venv/Scripts/python.exe"
        args: ["D:/SWMCP/mcp-server/server.py"]
        cwd: "D:/SWMCP"
        toolCallTimeoutMs: 600000
```

**错误写法**（本次踩过）：把 `- id: ...` 直接写在顶层。

顶层项的含义是“覆盖某个已存在插件的配置”，id 不存在时会被**静默忽略**——不报错、工具也不出现，很难排查。

## 排错顺序

1. 改完必须**重启**应用；插件在启动时加载。
2. 重启后开**新会话**：工具集在会话创建时绑定，旧会话不会刷新。
3. 仍看不到工具时，检查是否漏了 `insert:`。
4. 检查 `command` 路径是否可执行、`cwd` 是否存在。
5. 必要时设 `failOnStartupError: true`，让失败显式化。

## 工具命名

服务器名作为命名空间：`mcp__<serverName>__<tool>`。设 `serverName: solidworks` 时得到 `mcp__solidworks__...`。

## 超时

`toolCallTimeoutMs` 默认 60000 ms。CAD/CAE 操作常超过此值（打开大型装配体 10 s 起，重建更久），建议按实际操作放大。

## 验证

用最小调用确认链路：先 `connect` 类工具（只读、不改文件），再执行任何写操作。
