### ![blitz.io](http://blitz.io/images/logo2.png)

### Make load and performance a fun sport.

* Run a sprint from around the world
* Rush your API and website to scale it out
* Condition your site around the clock

## Getting started

Login to [blitz.io](http://blitz.io) and in the blitz bar type:
    
    --api-key

Then download and:

    python setup.py install

Or:

    easy_install blitz

And finally:

**Sprint**

```javascript
def callback(result):
    print("\nstatus: " + str(result.response.status))
    print("\nregion: " + result.region)
    print("\nduration: " + str(result.duration))
    print("\nconnect: " + str(result.connect))

options = {'url': "http://your.cool.app"}
s = Sprint("your@account.com", "aqbcdge-sjfkgurti-sjdhgft-skdiues")
s.execute(options, callback)
```

**Rush**

```javascript
def callback(result):
    for point in result.timeline:
        print("[")
        print("total:"+ str(point.total))
        print(", errors: " + str(point.errors))
        print(", hits: " + str(point.hits))
        print("]\n");

options = {'url': "http://your.cool.app",
    'pattern': { 'intervals': [{'start':1, 'end':50, 'duration':30}]}}
r = Rush("your@account.com", "aqbcdge-sjfkgurti-sjdhgft-skdiues")
r.execute(options, callback)    
```