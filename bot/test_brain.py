from bot.brain import CommandBrain, push_alpha_event

# Simulate a manual alpha trigger
push_alpha_event("TEST123", "Test Token")

# Instantiate and process
brain = CommandBrain()
brain.analyze_alpha()

# Simulate BirdEye fetch test
brain.simulate_birdeye_trades()
