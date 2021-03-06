/*
 * Copyright (c) 2017-2018 Intel Corporation
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

package com.intel.podm.common.utils;

public final class Casts {
    private Casts() {
    }

    public static <T> T tryCast(Object object, Class<T> clazz) {
        if (clazz.isInstance(object)) {
            return (T) object;
        } else {
            throw new ClassCastException("Couldn't convert " + object + " to " + clazz);
        }
    }
}
