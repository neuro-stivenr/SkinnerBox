# SkinnerBox

## Design

```python
experiment = Design([

    Message('Please press ENTER to continue.'),

    Trial([
        FixedRatio(ratio=10),
        VariableRatio(mean=10, sd=3),
        FixedInterval(interval=20),
        VariableInterval(mean=20, sd=6)
    ], t=300),

    Message('Please press ENTER to continue.'),

    Trial([
        FixedRatio(ratio=10),
        VariableRatio(mean=10, sd=3),
        FixedInterval(interval=20),
        VariableInterval(mean=20, sd=6)
    ], t=150),

    Message('Please press ENTER to continue.'),

    Trial([
        FixedRatio(ratio=10),
        VariableRatio(mean=10, sd=3),
        FixedInterval(interval=20),
        VariableInterval(mean=20, sd=6)
    ], t=150)

    Message('Please press ENTER to continue.'),

])

experiment.run()
```

You declare the design of your experiemnt as a list of Trials. Each trial itself consists of a list of reinforcement schedules, and t, which indicates the length of the trial in seconds.

When experiment.run() is called, a PyGame window is created, with a circular arrangement of options represented as circles, one corresponding to each schedule of reinforcement. On each circle is a number, corresponding to a numerical key on the keyboard. When a key is pressed, the corresponding circle briefly lights up in yellow, to indicate that it has been pressed.

Here's what happens when a key is pressed:

```python
# context
schedule = FixedRatio(ratio=5)

# press
schedule.press() # return False
result = [schedule.press() for i in range(5)]
result # [False, False, False, True, False]
```

When True is returned by a schedule, it is handled by the game, and increments the player's points, lighting up the point counter in the center of the circle to make them aware of the fact. Below the points counter can also be a timer.
