# Python-ArnoldC

Python implementation of [ArnoldC](https://github.com/lhartikk/ArnoldC)


## Installation

`pip install arnoldc`

## Usage

**HelloWorld.arnoldc**

```ArnoldC
IT'S SHOWTIME
TALK TO THE HAND "hello world"
YOU HAVE BEEN TERMINATED
```

```bash
$ arnoldc examples/HelloWorld.arnoldc
$ arnoldc --example
IT'S SHOWTIME
TALK TO THE HAND "Hello World!"
YOU HAVE BEEN TERMINATED
$ arnoldc --example | arnoldc
$ arnoldc -c <<EOF
> IT'S SHOWTIME
> TALK TO THE HAND "Hello World!"
> YOU HAVE BEEN TERMINATED
> EOF
Hello World!
```

## Language Documentation

[Official ArnoldC documentation](https://github.com/lhartikk/ArnoldC/wiki/ArnoldC)
