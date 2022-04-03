from experiment import Design, Message, DynamicProbTrial
from schedules import ProbRatioBlock

my_experiment = Design([
    Message('Press ENTER to start.'),
    DynamicProbTrial(
        [0.1, 0.15, 0.2, 0.25, 0.3, 0.6],
        t=120, warmup=75, inequality_threshold=2.0
    ),
    Message('Press ENTER to exit.')
])

my_experiment.run()