# 项目代码目录

BeeFintech 官网代码已放在本目录下，结构如下：

```text
src/
├── frontend/         静态 H5 官网页面与前端验证脚本
├── public/           官网静态资源
└── deploy/           部署说明
```

## 运行方式

直接打开：

```text
src/frontend/index.html
```

## 预约 API

预约表单在前端直接提交到：

```text
https://api.lifebee.tech/api/v3/gateway/booking
```

提交格式为 `application/x-www-form-urlencoded`，字段为 `name`、`phone`、`email`。

## 验证

```bash
cd src/frontend
npm test
```
