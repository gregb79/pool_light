
#include "pool_light.h"

namespace esphome {
namespace pool_light {

void PoolLight::setup() {
  // nothing special on setup for now
}

void PoolLight::write_state(bool state) {
  if (state) {
    this->send_command_();
  }
}

void PoolLight::send_command_() {
  // Prepare data packet (12 bytes)
  uint8_t DATA_TABLE[12] = {0xAA, 0xAA, 0xAA, 0xAA, 0x2D, 0xD4, 0xF9, 0xCB, 0x00, 17, 3, 0x00};

  // Apply configured values
  DATA_TABLE[6] = this->id0_;
  DATA_TABLE[7] = this->id1_;
  DATA_TABLE[9] = this->instruction_;
  DATA_TABLE[10] = this->mode_;

  // Calculate checksum
  uint16_t sum = 0;
  for (int i = 4; i < 11; i++) {
    sum += DATA_TABLE[i];
  }
  DATA_TABLE[11] = static_cast<uint8_t>(-sum);

  // Convert bytes to timing vector for CC1101 raw transmit (105us = 1, -104us = 0)
  std::vector<int> pulse_vector;
  for (int i = 0; i < 12; i++) {
    for (int bit = 7; bit >= 0; bit--) {
      bool bit_set = DATA_TABLE[i] & (1 << bit);
      pulse_vector.push_back(bit_set ? 105 : -104);
    }
  }

  // Transmit using CC1101 raw interface (repeat 5 times)
  for (int r = 0; r < 5; r++) {
    this->cc1101_->transmit_raw(pulse_vector);
    delay(10);  // small gap between repeats
  }

  ESP_LOGI("pool_light", "Command sent with ID0: 0x%02X ID1: 0x%02X Instruction: %d Mode: %d",
           this->id0_, this->id1_, this->instruction_, this->mode_);
}

}  // namespace pool_light
}  // namespace esphome
