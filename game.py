from experiment import Design, Trial, Message
from schedules import ProbRatioBlock

my_experiment = Design([
    Message('Press ENTER to continue.'),
    Trial(ProbRatioBlock([0.1, 0.2, 0.5, 0.3]), t=20),
    Message('Press ENTER to continue.'),
    Trial(ProbRatioBlock([0.1, 0.2, 0.5, 0.3, 0.8]), t=20),
    Message('Press ENTER to continue.'),
    Trial(ProbRatioBlock([0.9, 0.5, 0.3, 0.8]), t=20),
    Message('Experiment completed. Press ENTER to exit.')
])

my_experiment.run()