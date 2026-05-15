# 测试文档（M8a）

## 测试对象

本次测试对象是 BeeFintech 保险科技营销官网，代码位于 `src/frontend/index.html`，静态资源位于 `src/public/assets/`。页面为单页 H5 官网，包含顶部导航、Hero、Bee AI 演示、产品展示、平台能力、安全背书、客户评价、奖项资质、公司介绍、CTA 和预约弹窗。预约表单已从本地 mock 改为前端直接提交 Gateway Booking API。

## 桌面浏览器测试

| 测试项 | 结果 | 说明 |
| --- | --- | --- |
| 页面打开 | 通过 | 使用 in-app browser 打开 `src/frontend/index.html`，页面标题为 `Concept D - Bluechip Editorial`。 |
| 主要内容渲染 | 通过 | Hero 文案 `The InsurTech platform Hong Kong's brokers trust.` 可见。 |
| 静态资源 | 通过 | Logo 图片 1 张、Awards 图片 6 张均可被页面识别，控制台无资源加载错误。 |
| 导航与锚点 | 通过 | 顶部 `Book a demo` 可打开预约弹窗，`Try Bee AI` 可跳转到 AI demo 区域。 |
| 多语言基础状态 | 通过 | 页面保留 English、简体中文、繁体中文切换入口，语言菜单可展开。 |

## Bee AI 演示测试

AI demo 区域保留三种模式：`Compare products`、`Visualize a scenario`、`Ask Bee anything`。测试中确认输入框、提交按钮、额度显示和本地 `localStorage` 额度状态存在。提交问题后，页面会生成固定演示回答；额度用完时会引导打开预约弹窗。该部分是公开演示，不调用真实 AI 后端，因此不存储用户输入。

## 预约表单 API 测试

预约弹窗字段为 `name`、`phone`、`email`，均为必填。前端提交方式：

```text
POST https://api.lifebee.tech/api/v3/gateway/booking
Content-Type: application/x-www-form-urlencoded;charset=UTF-8
```

自动化检查使用：

```bash
cd src/frontend
npm test
```

测试结果：`frontend booking integration test passed`。该测试确认页面直接指向 Gateway API，不再经过 `/api/booking` 后端代理，并确认请求格式是 `application/x-www-form-urlencoded`。

真实 API 返回验证使用了带时间戳的测试数据，避免触发 10 分钟重复提交限制。接口返回：

```json
{
  "status": 200,
  "code": 1000,
  "message": null,
  "timestamp": "1778852892",
  "path": null,
  "data": true
}
```

页面表单测试中，成功后 `#demoSuccess` 进入 `visible` 状态，表单被隐藏，并显示 `We have received your booking request. We will contact you within one business day.`。浏览器控制台没有 error 或 warning。

## 已知限制

本仓库的 `scripts/check_milestones.py` 需要 Python 环境，但当前 Windows 环境没有 `python` 或 `py` 命令，因此未能本地运行 milestone 脚本。已使用前端测试脚本和浏览器实际操作完成验证。移动端 Safari、Android Chrome、微信内置浏览器尚未在真机上复测，后续上线前应补充真机截图。
