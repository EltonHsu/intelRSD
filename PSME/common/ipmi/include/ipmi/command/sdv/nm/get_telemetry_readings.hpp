/*!
 * @brief GetTelemetryReadings IPMI command request and response.
 *
 * @header{License}
 * @copyright Copyright (c) 2017 Intel Corporation.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * @header{Filesystem}
 * @file ipmi/command/sdv/nm/get_telemetry_readings.hpp
 */

#pragma once

#include "ipmi/request.hpp"
#include "ipmi/response.hpp"
#include "ipmi/command/sdv/enums.hpp"
#include "reading.hpp"

namespace ipmi {
namespace command {
namespace sdv {

namespace request {

/*!
 * @brief Request message for GetTelemetryReadings command.
 */
class GetTelemetryReadings : public Request {
public:
    /*!
     * @brief Constructor.
     */
    GetTelemetryReadings();


    GetTelemetryReadings(const GetTelemetryReadings&) = default;


    GetTelemetryReadings(GetTelemetryReadings&&) = default;


    GetTelemetryReadings& operator=(const GetTelemetryReadings&) = default;


    virtual ~GetTelemetryReadings();


    const char* get_command_name() const override {
        return "GetTelemetryReadings";
    }

    /*
     * @brief Reading package selector
     * @param package_guid ReadingPackage identifier
     */
    void set_package_guid(std::uint32_t package_guid) {
        m_package_guid = package_guid;
    }

    /*
     * @brief Start reading index setter.
     * @param start_reading_index Index of first reading to be retrieved (zero based)
     */
    void set_start_reading_index(std::uint8_t start_reading_index) {
        m_start_reading_index = start_reading_index;
    }

private:
    std::uint32_t m_package_guid{0};
    std::uint8_t m_start_reading_index{0};

    void pack(IpmiInterface::ByteBuffer& data) const override;
};

}

namespace response {

/*!
 * @brief Response message for GetTelemetryReadings command.
 */
class GetTelemetryReadings : public Response {
public:

    /*!
     * @brief Constructor.
     */
    GetTelemetryReadings();


    GetTelemetryReadings(const GetTelemetryReadings&) = default;


    GetTelemetryReadings(GetTelemetryReadings&&) = default;


    virtual ~GetTelemetryReadings();


    const char* get_command_name() const override {
        return "GetTelemetryReadings";
    }

    using RawReadingValues = std::vector<std::uint32_t>;

    /*!
     * @brief Returns metric reading collection.
     * @return Collection of metric readings.
     */
    const RawReadingValues& get_readings() const {
        return m_raw_readings;
    }

    /*
     * @brief Returns Next reading index.
     * The index of the next not returned reading or 0 if all readings returned.
     *
     * @return Next reading index
     */
    std::uint8_t get_next_reading_index() const {
        return m_next_reading_index;
    }

private:
    static constexpr const std::size_t MIN_RESPONSE_SIZE = 5;
    std::uint8_t m_next_reading_index{};
    RawReadingValues m_raw_readings{};

    void unpack(const IpmiInterface::ByteBuffer& data) override;

    void throw_error_on_completion_code(CompletionCode completion_code) const override;
};

}

}
}
}
