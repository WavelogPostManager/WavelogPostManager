# WavelogPostManager
QSL cards post status management for Wavelog.

> This project is under development.

### Installation

> `Python>=3.10`   

```shell
pip3 install wavelogpostmanager
```

```shell
pip3 install -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple wavelogpostmanager
```
*Dev*  

```shell
pip3 install -i https://test.pypi.org/simple/ wavelogpostmanager
```


### Run

```shell
wpm -init    # 安装后先初始化
wpm -start   # 启动Web服务器
wpm -q       # 将Wavelog中已排队的卡片进行制作信封
wpm -c       # 通讯录管理
wpm -s       # 查看已发出的QSL卡片信息
wpm -v       # 查看版本
```

这个项目还在内测当中，如有任何问题，欢迎在issues中提出，或到[QQ群](https://qm.qq.com/q/p7hWsqZ7ji)进行交流。