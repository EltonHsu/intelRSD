/*
 * Copyright (c) 2017 Intel Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.intel.podm.business.redfish.services;

import com.intel.podm.business.BusinessApiException;
import com.intel.podm.business.redfish.ServiceTraverser;
import com.intel.podm.business.services.context.Context;
import com.intel.podm.business.services.redfish.CreationService;
import com.intel.podm.common.synchronization.TaskCoordinator;
import com.intel.podm.common.types.redfish.RedfishEthernetSwitchAclRule;

import javax.enterprise.context.RequestScoped;
import javax.inject.Inject;
import javax.transaction.Transactional;
import java.util.concurrent.TimeoutException;

import static javax.transaction.Transactional.TxType.NEVER;

@RequestScoped
public class EthernetSwitchAclRuleCreationServiceImpl implements CreationService<RedfishEthernetSwitchAclRule> {
    @Inject
    private TaskCoordinator taskCoordinator;

    @Inject
    private ServiceTraverser traverser;

    @Inject
    private EthernetSwitchAclRuleActionsService ethernetSwitchAclRuleActionsService;

    @Override
    @Transactional(NEVER)
    public Context create(Context creationalContext, RedfishEthernetSwitchAclRule representation) throws BusinessApiException, TimeoutException {
        return taskCoordinator.call(
            traverser.traverseServiceUuid(creationalContext),
            () -> ethernetSwitchAclRuleActionsService.create(creationalContext, representation)
        );
    }
}
