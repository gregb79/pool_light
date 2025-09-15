import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button, cc1101
from esphome.const import CONF_ID, CONF_NAME

POOL_LIGHT_NS = cg.esphome_ns.namespace('pool_light')
PoolLightButton = POOL_LIGHT_NS.class_('PoolLightButton', button.Button, cg.Component)

CONFIG_SCHEMA = button.button_schema(  # base button schema
    cv.Schema({
        cv.Required(CONF_ID): cv.declare_id(PoolLightButton),
        cv.Required(CONF_NAME): cv.string,
        cv.Required('id0'): cv.uint8_t,
        cv.Required('id1'): cv.uint8_t,
        cv.Required('instruction'): cv.string,
        cv.Required('mode'): cv.string,
        cv.Required('cc1101_module'): cv.use_id(cc1101.CC1101Component),
    })
).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID], config[CONF_NAME])
    await cg.register_component(var, config)
    await button.register_button(var, config)
    cg.add(var.set_id0(config['id0']))
    cg.add(var.set_id1(config['id1']))
    cg.add(var.set_instruction(config['instruction']))
    cg.add(var.set_mode(config['mode']))
    cc = await cg.get_variable(config['cc1101_module'])
    cg.add(var.set_cc1101_module(cc))
