#pragma once

#include "esphome.h"
#include "esphome/components/button/button.h"
#include "esphome/components/cc1101/cc1101.h"

namespace esphome {
namespace pool_light {

class PoolLight : public button::Button, public Component {
 public:
  void setup() override;
  void write_state(bool state) override;

  void set_id0(uint8_t id0) { this->id0_ = id0; }
  void set_id1(uint8_t id1) { this->id1_ = id1; }
  void set_instruction(uint8_t instruction) { this->instruction_ = instruction; }
  void set_mode(uint8_t mode) { this->mode_ = mode; }
  void set_cc1101_module(cc1101::CC1101Component *cc1101) { this->cc1101_ = cc1101; }

 protected:
  cc1101::CC1101Component *cc1101_;
  uint8_t id0_ = 0xF9;          // default 249 decimal
  uint8_t id1_ = 0xCB;          // default 203 decimal
  uint8_t instruction_ = 17;    // default "power"
  uint8_t mode_ = 3;            // default "pool and spa 3"

  void send_command_();
};

}  // namespace pool_light
}  // namespace esphome
