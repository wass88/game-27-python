# Game 27 Simple AI

手元で対戦をする場合は https://github.com/wass88/game-ai/releases

```
$ ./playout game27 "python main.py" "python main.py"
```

ゲームルールは https://github.com/wass88/game-27-ai

```
$ docker build . -t game-27-python
$ docker run --rm -it game-27-python
```