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

#include "mobile-client-strategy.hpp"
#include "ns3/ndnSIM/NFD/daemon/fw/algorithm.hpp"

namespace nfd {
namespace fw {

NFD_LOG_INIT("MobileClientStrategy");

const Name MobileClientStrategy::STRATEGY_NAME("ndn:/localhost/nfd/strategy/mobile-client/%FD%01");

int MobileClientStrategy::timerMilliseconds(999); // initialize the timer duration with 1 second

NFD_REGISTER_STRATEGY(MobileClientStrategy);



MobileClientStrategy::MobileClientStrategy(Forwarder& forwarder, const Name& name)
  : Strategy(forwarder, name)
{

}



void
MobileClientStrategy::afterReceiveInterest(const Face& inFace, const Interest& interest,
                   const shared_ptr<pit::Entry>& pitEntry)
{

  // starting the timer for the first time
  if (isFirstTimer == true) {
    isFirstTimer == false;
    if (isTimerRunning == false) {
      isTimerRunning = true;
      time::nanoseconds timerTime = time::milliseconds(timerMilliseconds);
      this->forwardingDecisionTimer = scheduler::schedule(timerTime, bind(&MobileClientStrategy::onTimerTimedOut, this));
    }
  }


  // get face ID with the highest Interest Satisfaction Ratio
  std::string faceIdString = getMaxISRFaceId(isr);
  int faceIdInt = stoi(faceIdString);


  if (isr[faceIdString] < isrThreshold) { // sending IP out on all faces

    // counts each Interest Packet only once - in interestCounter
    bool interestCounterUpdated = false;

    const fib::Entry& fibEntry = this->lookupFib(*pitEntry);
    const fib::NextHopList& nexthops = fibEntry.getNextHops();

    for (fib::NextHopList::const_iterator it = nexthops.begin(); it != nexthops.end(); ++it) {

      Face& outFace = it->getFace();

      // sending IP
      if (!wouldViolateScope(inFace, interest, outFace) &&
        canForwardToLegacy(*pitEntry, outFace)) {
        this->sendInterest(pitEntry, outFace, interest);

        // counts each IP once
        if (interestCounterUpdated == false) {
          interestCounter = interestCounter + 1;
          interestCounterUpdated = true;
        }

        // counts all IP
        std::string interestPrefix = interest.getName().getPrefix(1).toUri(); // prefix
        std::string outFaceIdString = std::to_string(outFace.getId()); // outgoing face ID string
        updateCounter(interestPrefix, outFaceIdString, allInterestCounter);

      } // end if
    } // end for



  } else { // sending IP out on best face

    const fib::Entry& fibEntry = this->lookupFib(*pitEntry);
    const fib::NextHopList& nexthops = fibEntry.getNextHops();

    for (fib::NextHopList::const_iterator it = nexthops.begin(); it != nexthops.end(); ++it) {

      Face& outFace = it->getFace();
      int outFaceInt = outFace.getId();

      // sending IP
      if (faceIdInt == outFaceInt && !wouldViolateScope(inFace, interest, outFace) && canForwardToLegacy(*pitEntry, outFace)) {
        this->sendInterest(pitEntry, outFace, interest);

        // counts each IP once
        interestCounter = interestCounter + 1;

        // counts al IP (in this case each IP once)
        std::string interestPrefix = interest.getName().getPrefix(1).toUri(); // prefix
        std::string outFaceIdString = std::to_string(outFace.getId()); // outgoing face ID string
        updateCounter(interestPrefix, outFaceIdString, allInterestCounter);

      } // end if
    } // end for
  } // end else

}



void
MobileClientStrategy::beforeSatisfyInterest(const shared_ptr<pit::Entry>& pitEntry,
                                   const Face& inFace, const Data& data)
{

  std::string dataPrefix = data.getName().getPrefix(1).toUri(); // prefix
  std::string inFaceIdString = std::to_string(inFace.getId()); // incomming face ID string

  // counts each DP once
  if (pitEntry->isSatisfied() == false) {
    updateCounter(dataPrefix, inFaceIdString, dataCounter);
    pitEntry->setSatisfied(true);
  }

  // counts all DP
  updateCounter(dataPrefix, inFaceIdString, allDataCounter);

}



std::string
MobileClientStrategy::getMaxISRFaceId(std::map<std::string, int> isr) {

  std::string maxFaceId = "-1";
  int maxIsrValue = -1;

  for(auto elem : isr) {

    if (elem.second > maxIsrValue) {
      maxFaceId = elem.first;
      maxIsrValue = elem.second;
    }
  }

  return maxFaceId;

}



void
MobileClientStrategy::updateCounter(std::string packetPrefix, std::string faceId, std::map<std::string, std::map<std::string, int>>& packetsCounter)
{

  // checks if the prefix is already in the map <prefix, <face, counter>>
  if (packetsCounter.count(packetPrefix)) { // prefix is already in map

    // checks if the face is already in the map <prefix, <face, counter>>
    if (packetsCounter[packetPrefix][faceId]) { // face is already in map
      packetsCounter[packetPrefix][faceId] = packetsCounter[packetPrefix][faceId] + 1;

    } else { // face is not in map
      packetsCounter[packetPrefix][faceId] = 1;
    }

  } else { // prefix is not in map
    packetsCounter[packetPrefix][faceId] = 1;
  }

}



void
MobileClientStrategy::onTimerTimedOut()
{

  // the timer has been timed out (stopped)
  scheduler::cancel(this->forwardingDecisionTimer);
  isTimerRunning = false;

  // calculate the forwarding decision
  calculateForwardingDecision();

  // starting the timer
  if (isTimerRunning == false) {
    isTimerRunning = true;
    time::nanoseconds timerTime = time::milliseconds(timerMilliseconds);
    this->forwardingDecisionTimer = scheduler::schedule(timerTime, bind(&MobileClientStrategy::onTimerTimedOut, this));
  }

}



void
MobileClientStrategy::calculateForwardingDecision()
{

  // calculates ISR for all faces together ---> isrValue is not used
  int isrValue = getISRAllFaces(interestCounter, dataCounter);

  // calculates ISR for each face separately
  isr = getISRFace(allInterestCounter, allDataCounter);

  // clears all IP and DP counters
  interestCounter = 0;
  refreshCounters(dataCounter);
  refreshCounters(allInterestCounter);
  refreshCounters(allDataCounter);

}



void
MobileClientStrategy::refreshCounters(std::map<std::string, std::map<std::string, int>>& packetsCounter)
{
  packetsCounter.clear();
}



int
MobileClientStrategy::getISRAllFaces(int interestCounter, std::map<std::string, std::map<std::string, int>>& dataCounter)
{

  int numberOfInterestPackets = interestCounter;
  int numberOfDataPackets = 0;

  // calculate the number of DPs
  for(auto dataElem1 : dataCounter) {
    for(auto dataElem2 : dataElem1.second) {
      numberOfDataPackets = numberOfDataPackets + dataElem2.second;
    }
  }

  // calculate ISR
  int isrValue = calculateISR(numberOfInterestPackets, numberOfDataPackets);

  return isrValue;

}



std::map<std::string, int>
MobileClientStrategy:: getISRFace(std::map<std::string, std::map<std::string, int>>& interestCounter, std::map<std::string, std::map<std::string, int>>& dataCounter) {

  // this is needed to count all packets together from different prefixes
  std::map<std::string, int> faceInterestCounter; // <face ID, #IP>
  std::map<std::string, int> faceDataCounter; // <face ID, #DP>

  std::map<std::string, int> faceIsr; // <face ID, ISR>


  // counts all interest packets from <prefix, <face ID, #IP>> to <face ID, #IP
  for(auto interestElem1 : interestCounter) {
    for(auto interestElem2 : interestElem1.second) {

      if (faceInterestCounter[interestElem2.first]) { // face is already in map
        faceInterestCounter[interestElem2.first] = faceInterestCounter[interestElem2.first] + interestElem2.second;

      } else { // face is not in map
        faceInterestCounter[interestElem2.first] = interestElem2.second;
      }
    } // end for
  } // end for


  // counts all data packets from <prefix, <face ID, #DP>> to <face ID, #DP>
  for(auto dataElem1 : dataCounter) {
    for(auto dataElem2 : dataElem1.second) {

      if (faceDataCounter[dataElem2.first]) { // face is already in map
        faceDataCounter[dataElem2.first] = faceDataCounter[dataElem2.first] + dataElem2.second;

      } else { // face is not in map
        faceDataCounter[dataElem2.first] = dataElem2.second;
      }
    } // end for
  } // end for


  // calculates the ISR for each face <face ID, ISR>
  for(auto interestElem1 : faceInterestCounter) {
    faceIsr[interestElem1.first] = calculateISR(interestElem1.second, faceDataCounter[interestElem1.first]);

  }

  return faceIsr;

}



int
MobileClientStrategy::calculateISR(int numberOfInterests, int numberOfSatisfiedInterests) {

  if (numberOfInterests == 0) {
    return 0;

  } else {
    float isr = (float(numberOfSatisfiedInterests) / float(numberOfInterests)) * 100.0;
    return int(isr);
  }

}

} // namespace fw
} // namespace nfd
