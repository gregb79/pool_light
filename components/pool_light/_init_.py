
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button, cc1101
from esphome.const import CONF_ID

DEPENDENCIES = ['cc1101']

pool_light_ns = cg.esphome_ns.namespace('pool_light')
PoolLight = pool_light_ns.class_('PoolLight', button.Button, cg.Component)

CONF_ID0 = 'id0'
CONF_ID1 = 'id1'
CONF_INSTRUCTION = 'instruction'
CONF_MODE = 'mode'
CONF_CC1101_MODULE = 'cc1101_module'

INSTRUCTION_VALUES = {
    "power": 17,
    "blue": 33,
    "magenta": 34,
    "red": 35,
    "lime": 36,
    "green": 37,
    "aqua": 38,
    "white": 39,
    "mode1": 49,
    "mode2": 50,
    "mode3": 51,
    "mode4": 52,
    "brightness": 65,
}

MODE_VALUES = {
    "pool": 1,
    "spa": 2,
    "poolandspa": 3,
}

CONFIG_SCHEMA = button.BUTTON_SCHEMA.extend({
    cv.GenerateID(): cv.declare_id(PoolLight),
    cv.Optional(CONF_ID0, default=0xF9): cv.int_range(min=0x00, max=0xFF),
    cv.Optional(CONF_ID1, default=0xCB): cv.int_range(min=0x00, max=0xFF),
    cv.Optional(CONF_INSTRUCTION, default='power'): cv.one_of(*INSTRUCTION_VALUES.keys(), lower=True),
    cv.Optional(CONF_MODE, default='pool and spa 3'): cv.one_of(*MODE_VALUES.keys(), lower=True),
    cv.Required(CONF_CC1101_MODULE): cv.use_id(cc1101.CC1101Component),
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await button.register_button(var, config)

    id0 = config.get(CONF_ID0, 0xF9)
    id1 = config.get(CONF_ID1, 0xCB)
    instruction_str = config.get(CONF_INSTRUCTION, 'power').lower()
    mode_str = config.get(CONF_MODE, 'pool and spa 3').lower()

    instruction = INSTRUCTION_VALUES[instruction_str]
    mode = MODE_VALUES[mode_str]

    cg.add(var.set_id0(id0))
    cg.add(var.set_id1(id1))
    cg.add(var.set_instruction(instruction))
    cg.add(var.set_mode(mode))
    cg.add(var.set_cc1101(config[CONF_CC1101_MODULE]))
