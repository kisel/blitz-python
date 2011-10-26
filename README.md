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
    print("> Result:")
    print("\tregion: " + result.region)
    print("\tduration: " + str(result.duration))
    for step in result.steps:
        print("> Step:")
        print("\tstatus: " + str(step.response.status))
        print("\tduration: " + str(step.duration))
        print("\tconnect: " + str(step.connect))

options = {
    'steps':[
        {'url': "http://your.cool.app"},
        {'url': "http://your.cool.app/page1"}
    ]
}
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
        print(", steps: " + str(len(point.steps)))
        for step in point.steps:
            print("\tstep duration: " + str(step.duration))
        print("]\n");

options = {
    'steps':[
        {'url': "http://your.cool.app"},
        {'url': "http://your.cool.app/page1"}
    ],
    'pattern': { 'intervals': [{'start':1, 'end':50, 'duration':30}]}}
r = Rush("your@account.com", "aqbcdge-sjfkgurti-sjdhgft-skdiues")
r.execute(options, callback)    
```
