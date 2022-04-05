/**
 * Copyright (c) 2018,  Sandra-Nadine Bergmann (Alpen-Adria Universitaet Klagenfurt)
 *
 * This file is part of the ndnSIM extensions.
 *
 * NFD is free software: you can redistribute it and/or modify it under the terms
 * of the GNU General Public License as published by the Free Software Foundation,
 * either version 3 of the License, or (at your option) any later version.
 *
 * NFD is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
 * PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with
 * NFD, e.g., in COPYING.md file.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef NFD_DAEMON_FW_MOBILECLIENT_STRATEGY_HPP
#define NFD_DAEMON_FW_MOBILECLIENT_STRATEGY_HPP

#include "ns3/ndnSIM/NFD/daemon/fw/strategy.hpp"

namespace nfd {
namespace fw {

/**
 * @brief MobileClientStrategy contains a Forwarding Strategy used by mobile client nodes in ndnSIM where the decision of how to forward Interest Packets depends on the Interest Satisfaction Ratio.
 */
class MobileClientStrategy : public Strategy
{
public:
  explicit
  MobileClientStrategy(Forwarder& forwarder, const Name& name = STRATEGY_NAME);

  /**
  * @brief afterReceiveInterest is called when an Interest Packet is received.
  * @param inFace the incoming face where the Interest Packet is received.
  * @param interest the Interest Packet.
  * @param pitEntry the Pending Interest Table entry for the received Interest Packet.
  */
  virtual void
  afterReceiveInterest(const Face& inFace, const Interest& interest,
                       const shared_ptr<pit::Entry>& pitEntry) override;

  /**
  * @brief beforeSatisfyInterest is called when a Data Packet is received.
  * @param pitEntry the Pending Interest Table entry for the requested data.
  * @param inFace the incoming face where the Data Packet is received.
  * @param data the Data Packet.
  */
  virtual void
  beforeSatisfyInterest(const shared_ptr<pit::Entry>& pitEntry,
                        const Face& inFace, const Data& data) override;

  /**
  * @brief getMaxISRFaceId checks and gets the face ID with the highest Interest Satisfaction Ratio.
  * @param isr a map with the current Interest Satisfaction Ratio values.
  * @return the face ID with the higehest Interest Satisfaction Ratio.
  */
  std::string
  getMaxISRFaceId(std::map<std::string, int> isr);

  /**
  * @brief updateCounter updates a specific counter variable.
  * @param longPrefix the prefix of the packet.
  * @param faceId the face ID for which a packet is counted.
  * @param packetsCounter the counter variable.
  */
  void
  updateCounter(std::string longPrefix, std::string faceId, std::map<std::string, std::map<std::string, int>>& packetsCounter);

  /**
  * @brief onTimerTimedOut is called when the timer expires.
  */
  void
  onTimerTimedOut();

  /**
  * @brief calculateForwardingDecision is called when a decision has to be made where to forward further Interest Packets.
  */
  void
  calculateForwardingDecision();

  /**
  * @brief refreshCounters resets a specific counter variable.
  * @param packetsCounter the counter variable which should be cleared.
  */
  void
  refreshCounters(std::map<std::string, std::map<std::string, int>>& packetsCounter);

  /**
  * @brief getISRAllFaces calculates the Interest Satisfaction Ratio for all faces together.
  * @param interestCounter the number of outgoing Interest Packets.
  * @param dataCounter the number of satisfied Interest Packets through a Data Packet.
  */
  int
  getISRAllFaces(int interestCounter, std::map<std::string, std::map<std::string, int>>& dataCounter);

  /**
  * @brief getISRFace calculates the Interest Satisfaction Ratio for each face separately.
  * @param interestCounter the number of outgoing Interest Packets for each face.
  * @param dataCounter the number of satisfied Interest Packets through a Data Packet for each face.
  */
  std::map<std::string, int>
  getISRFace(std::map<std::string, std::map<std::string, int>>& interestCounter, std::map<std::string, std::map<std::string, int>>& dataCounter);

  /**
  * @brief calculateISR calculates the Interest Satisfaction Ratio.
  * @param numberOfInterests the number of outgoing Interest Packets.
  * @param numberOfSatisfiedInterests the number of Interest Packets which are satisfied through a Data Packet (incoming Data Packets).
  */
  int
  calculateISR(int numberOfInterests, int numberOfSatisfiedInterests);

  

public:
  static const Name STRATEGY_NAME;


protected:

  // the timer
  bool isTimerRunning = false; // true when the timer is already running
  static int timerMilliseconds; // the duration of the timer (in milliseconds)
  scheduler::EventId forwardingDecisionTimer = 0; // the scheduler for the timer
  bool isFirstTimer = true; // true, before the first fimer starts


  // the IP counters
  int interestCounter = 0; // counts each IP once
  std::map<std::string, std::map<std::string, int> > allInterestCounter; // counts all outgoing IPs at all faces

  // the DP counters
  std::map<std::string, std::map<std::string, int> > dataCounter; // counts each satisfied IP through a DP once (only first satisfaction)
  std::map<std::string, std::map<std::string, int> > allDataCounter; // counts all incoming DPs at all faces


  // variables for calculating the Interest Satisfaction Ratio
  int isrThreshold = 90; // the threshold for the Interest Satisfaction Ratio
  std::map<std::string, int> isr; // the Interest Satisfaction Ratio for each face stored in a map <face ID, ISR>

};

} // namespace fw
} // namespace nfd

#endif // NFD_DAEMON_FW_MOBILECLIENT_STRATEGY_HPP
