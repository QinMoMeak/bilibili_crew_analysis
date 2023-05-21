# bilibili_crew_analysis
b站直播间舰长分析

配置

  1.修改UID和self.ruid（根据UID获取ruid接口暂时测试失效）
  
  2.py3 安装所需依赖 运行
  
  3.命令行得到结果，用户名、UID、Level存入data.csv
  
自行修改

- 请求时间间隔调整 默认1s 避免IP封禁
- 增加IP池
- 获取用户其他信息 字段名称参考[bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/user/info.md?plain=1) 存于变量json_data（dict格式）
