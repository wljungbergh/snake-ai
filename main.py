from env.environment import *

if __name__ == "__main__":
    LEARNING_RATE = 0.01
    DISCOUT = 0.99
    EPISODES = 1000000


    se = SnakeEnv(size=20)
    se.game.reset(se.size)
    done = False
    render = True

    qtable = np.random.uniform(low = -0.001, high=0.001, size=(se.obs_size + [se.act_size]))
    epsilon = 0.05/0.9

    if render: se.pygame_init()

    for i in range(EPISODES):
        done = False
        
        state = se.game.get_state()
        if i%1000 == 0:
            if i%20000 == 0:
                #render = True
                #se.size += 1
                #epsilon *= 0.9
                LEARNING_RATE *= 0.96
            print("i: {}".format(i))
            print("eps: {}".format(epsilon))
        else:
            render = False
            
        while not done:
            if render:
                for event in pygame.event.get(): # User did something
                    if event.type == pygame.QUIT: # If user clicked close
                        carryOn = False # Flag that we are done so we exit this loop
            #action = np.random.randint(0,4,1)
            if np.random.uniform() < 0: #epsilon: 
                action = np.random.randint(0,se.act_size) 
            else:
                action_list = np.argsort(qtable[state])
                action = action_list[-1]
                if not se.game.valid_move(action):
                    action = action_list[-2]
                
        

            new_state, rew, done, info = se.step(action)
            
            
            
            if not done:
                max_future_q = np.max(qtable[new_state])
                current_q = qtable[state + (action,)]
                new_q = (1-LEARNING_RATE)*current_q + LEARNING_RATE * (rew + DISCOUT * max_future_q)
                qtable[state + (action,)] = new_q
                #print(rew)

            state = new_state
            if render:
                
                se.render()
                pygame.display.update()
                se.clock.tick(25)
                

        
        se.reset()

    pygame.quit()

    pickle.dump

    with open('qtable.pickle', 'wb') as f:
        pickle.dump(qtable, f)
        
