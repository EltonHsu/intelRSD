/*!
 * @copyright
 * Copyright (c) 2016-2017 Intel Corporation
 *
 * @copyright
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * @copyright
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * @copyright
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @file command/stubs/get_zone_info.cpp
 * @brief GetZoneInfo sdv implementation
 * */

#include "agent-framework/module/pnc_components.hpp"
#include "agent-framework/command/registry.hpp"
#include "agent-framework/command/pnc_commands.hpp"

using namespace agent_framework::command;
using namespace agent_framework::module;
using namespace agent_framework::model;

REGISTER_COMMAND(GetZoneInfo,
    [] (const GetZoneInfo::Request& req, GetZoneInfo::Response& rsp) {
        rsp = get_manager<Zone>().get_entry(req.get_uuid());
        log_debug(GET_LOGGER("pnc-gami"), "Getting ZoneInfo successful.");
    }
);
