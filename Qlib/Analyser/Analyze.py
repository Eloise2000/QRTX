from rtxlib import error, info
from Qlib.Knowledge.Knowledge import instance as knowledge_instance
import numpy as np

class Analyser:
    def __init__(self, wf):
        self.wf = wf


    def _defaultChangeProvider(self, variables):
        """ by default we just forword the message to the change provider """
        return variables

    def run(self):
        # apply changes to system
        try:
            self.wf.change_provider["instance"].applyChange(self._defaultChangeProvider(knowledge_instance.new_knob_val))
        except:
            error("apply changes did not work")

        info("< new exploration percentage applied: " + str(knowledge_instance.new_knob_val))

    def learn(self):
        for episode in range(num_episodes):
            observation = env.reset()   # 初始化本场游戏的环境
            state = digitize_state(observation)     # 获取初始状态值
            action = np.argmax(q_table[state])      # 根据状态值作出行动决策
            episode_reward = 0
            # 一场游戏分为一个个时间步
            for t in range(max_number_of_steps):
                env.render()    # 更新并渲染游戏画面
                observation, reward, done, info = env.step(action)  # 获取本次行动的反馈结果
                action, state = get_action(state, action, observation, reward)  # 作出下一次行动的决策
                episode_reward += reward
                if done:
                    print('%d Episode finished after %f time steps / mean %f' % (episode, t + 1, last_time_steps.mean()))
                    last_time_steps = np.hstack((last_time_steps[1:], [episode_reward]))  # 更新最近100场游戏的得分stack
                    break
                    # 如果最近100场平均得分高于195
                if (last_time_steps.mean() >= goal_average_steps):
                    print('Episode %d train agent successfuly!' % episode)
                    break
