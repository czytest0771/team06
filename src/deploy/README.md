# 部署说明

这是一个静态 H5 官网，可部署到任意静态托管服务。

## 入口

```text
src/frontend/index.html
```

## 静态资源

```text
src/public/assets/
```

当前页面通过相对路径 `../public/assets/...` 引用图片资源。如果部署平台要求统一静态资源目录，可将 `src/public/assets` 复制到站点根目录的 `public/assets` 或 `assets`，并同步调整 `index.html` 中的资源路径。

## 表单接口

预约表单由前端直接请求 Gateway API：

```text
POST https://api.lifebee.tech/api/v3/gateway/booking
Content-Type: application/x-www-form-urlencoded;charset=UTF-8
```

字段：

```text
name
phone
email
```
