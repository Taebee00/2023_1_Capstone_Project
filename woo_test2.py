def moveArmSlow(self):
    for i in range(3):
        angle_diff = self.target_angle[i] - self.current_angles[i]
        steps = abs(int(angle_diff / 3))
        direction = 1 if angle_diff > 0 else -1
        for j in range(steps):
            self.current_angles[i] += 3 * direction
            self.setPWMwithAngle(self.current_angles)
            time.sleep(0.2)
        remaining_angle_diff = abs(angle_diff) - (steps * 3)
        if remaining_angle_diff > 0:
            self.current_angles[i] += remaining_angle_diff * direction
            self.setPWMwithAngle(self.current_angles)
            time.sleep(0.2)
