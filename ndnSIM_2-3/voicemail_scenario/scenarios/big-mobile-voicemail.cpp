/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/**
 * Copyright (c) 2011-2015  Regents of the University of California.
 *
 * This file is part of ndnSIM. See AUTHORS for complete list of ndnSIM authors and
 * contributors.
 *
 * ndnSIM is free software: you can redistribute it and/or modify it under the terms
 * of the GNU General Public License as published by the Free Software Foundation,
 * either version 3 of the License, or (at your option) any later version.
 *
 * ndnSIM is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
 * PURPOSE.  See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with
 * ndnSIM, e.g., in COPYING.md file.  If not, see <http://www.gnu.org/licenses/>.
 **/

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/ndnSIM-module.h"

#include "../extensions/randnetworks/networkgenerator.h"
#include "boost/filesystem.hpp"

NS_LOG_COMPONENT_DEFINE("BigMobileVoicemail");

namespace ns3 {

/**
 * @brief addAndUpdateNodesToAPsMap updates a map which contains router nodes which are connected to APs as well as the number of connections to APs
 * @param nodeMap a map, which contains a router node and the number of connections to APs
 * @param node the node to add or update in the map
 */
void
addAndUpdateNodesToAPsMap(std::map<Ptr<Node>, int>& nodeMap, Ptr<Node> node) {

  if (!nodeMap[node]) {
    nodeMap[node] = 1;

  } else {
    for (auto n : nodeMap) {
      if (n.first == node) {
        nodeMap[n.first] = n.second + 1;
      }
    }
  }

}

int
main(int argc, char* argv[])
{

  // 1) forwarding strategies

  // all possible forwarding strategies
  std::string bestRouteFWStrategyName = "best-route";
  std::string multicastFWStrategyName = "multicast";
  std::string mobileClientFWStrategyName = "mobile-client";

  std::string bestRouteForwardingStrategy = "/localhost/nfd/strategy/" + bestRouteFWStrategyName;
  std::string multicastForwardingStrategy = "/localhost/nfd/strategy/" + multicastFWStrategyName;
  std::string mobileClientForwardingStrategy = "/localhost/nfd/strategy/" + mobileClientFWStrategyName;

  // forwarding strategy for the mobile client nodes, default is best-route
  std::string clientForwardingStrategyName = bestRouteFWStrategyName;
  std::string clientForwardingStrategy = bestRouteForwardingStrategy;



  // 2) files and directories
  std::string confFile = "brite_configs/brite_3_as.conf";

  std::string logDir = "results/big-mobile-voicemail/";

  std::string rateTraceFile = "rate-trace.txt";
  std::string appDelayTraceFile = "app-delays-trace.txt";
  std::string callLengthFile = "callLengths.txt";



  // 3) additional variables for command line parameters (number of APs, position of APs, ISR threshold)

  // number of APs for each WiFi network  
  int noAPs = 1;

  // set the x-position and y-position for APs
  int xPosWiFi = 15; // (15) or 20
  int yPosWiFi = -150;

  // set the next y-position for the next AP
  int yPosNextAP = -30; // (-30) or -40

  // set ISR Threshold (important: set in forwarding strategy as well, here only for folder name of simulation output)
  int isrThreshold = 90;



  // 4) command line parameters
  CommandLine cmd;
  cmd.AddValue("briteConfig", "The path to the BRITE configuration file [default=brite_configs/brite_3_as.conf].", confFile);
  cmd.AddValue("logDir", "The path to the folder where files are saved [default=results/big-mobile-voicemail/].", logDir);
  cmd.AddValue("fwStrategy", "The used forwarding strategy for the mobile client nodes [default=best-route].", clientForwardingStrategyName);
  cmd.AddValue("noAPs", "The number of AP nodes for each WiFi network [default=1].", noAPs);
  cmd.AddValue("xPos", "The APs x position [default=20].", xPosWiFi);
  cmd.AddValue("yPos", "The APs y position [default=-150].", yPosWiFi);
  cmd.AddValue("yPosNext", "The next APs y position [default=-40].", yPosNextAP);
  cmd.AddValue("isrT", "The ISR Threshold [default=90].", isrThreshold);
  cmd.Parse(argc, argv);

  // set mobile client forwarding strategy
  if (clientForwardingStrategyName == bestRouteFWStrategyName) {
    clientForwardingStrategy = bestRouteForwardingStrategy;

  } else if (clientForwardingStrategyName == multicastFWStrategyName) {
    clientForwardingStrategy = multicastForwardingStrategy;

  } else if (clientForwardingStrategyName == mobileClientFWStrategyName) {
    clientForwardingStrategy = mobileClientForwardingStrategy;

  } else {
     //do nothing
  }

  // create all directories if not exist
  // TODO: only needed when executing without python script to create the folde before (works not on server - maybe different library versions)
  //if (!boost::filesystem::exists(logDir)) {
   //boost::filesystem::create_directories(logDir);
  //}



  // 5) variables for generating a random network with BRITE using the config file

  // queue
  std::string queueNameGen = "DropTail_Bytes";
  uint32_t queueSize = 50;
  std::string queue = "ns3::DropTailQueue";
  std::string queueMode = "QUEUE_MODE_BYTES";

  // network parameters for medium connectivity
  int minBWInter = 3000;
  int maxBWInter = 5000;
  int minDelayInter = 5;
  int maxDelayInter = 15;
  int numberOfConnectionsInter;

  int minBWIntra = 2000;
  int maxBWIntra = 4000;
  int minDelayIntra = 5;
  int maxDelayIntra = 15;
  int numberOfConnectionsIntra;



  // 6) point to point helper link for adding new links between a network node and APs bzw. a network node and fixed client nodes
  PointToPointHelper *p2p = new PointToPointHelper;
  p2p->SetDeviceAttribute ("DataRate", StringValue ("4Mbps"));
  p2p->SetChannelAttribute ("Delay", StringValue ("5ms"));
  p2p->SetQueue(queue, "Mode", StringValue(queueMode), "MaxBytes", StringValue(boost::lexical_cast<std::string>(queueSize * 1000)));



  // 7) AP nodes for for the WiFi networks
  int numberOfAPs = noAPs;

  // first WiFi
  int xPosFirstWifi = -xPosWiFi;
  int yPosFirstWifi = yPosWiFi;
  std::string firstWifiAPs = "FirstWifi_AP";
  std::string routersOfFirstWifiAPs = "Router_" + firstWifiAPs;

  NodeContainer firstWifiAPNodes;
  NodeContainer routersOfFirstWifiAPNodes;

  // second WiFi
  int xPosSecondWifi = xPosWiFi;
  int yPosSecondWifi = yPosWiFi;
  std::string secondWifiAPs = "SecondWifi_AP";
  std::string routersOfSecondWifiAPs = "Router_" + secondWifiAPs;

  NodeContainer secondWifiAPNodes;
  NodeContainer routersOfSecondWifiAPNodes;



  // 8) client nodes
  // set number of clients
  int numberOfClients = 10;

  // fixed client nodes
  int numberOfFixedClients = numberOfClients;
  std::string fixedClientName = "Fixed_Client";
  NodeContainer fixedClientNodes;

  // mobile client nodes
  int numberOfMobileClients = numberOfClients;
  std::string mobileClientName = "Mobile_Client";
  NodeContainer mobileClientNodes;

  // mobile client nodes position
  // set the mobile client nodes start position
  int mobileClientPosX = 0;
  int mobileClientPosY = yPosWiFi;

  // set the mobile client nodes moving area from start position
  // x position
  int edge = 10;
  int mobileClientMinX = -xPosWiFi - edge;
  int mobileClientMaxX = xPosWiFi + edge;

  // y position
  int mobileClientMinY = 0;
  if (numberOfAPs == 1) {
    mobileClientMinY = -edge;
  } else {
    mobileClientMinY = numberOfAPs * yPosNextAP/2 - edge;
  }
  int mobileClientMaxY = edge;

  // mobility models
  // set mobileClientMobilityModel
  std::string gaussMarkovMobilityModel = "ns3::GaussMarkovMobilityModel";
  std::string randomWaypointMobilityModel = "ns3::RandomWaypointMobilityModel";
  std::string constantPositionMobilityModel = "ns3::ConstantPositionMobilityModel";
  std::string mobileClientMobilityModel = gaussMarkovMobilityModel;



  // 9) WiFi links
  // set WiFi parameters

  // WiFi standard A
  enum WifiPhyStandard wifiStandardA = WIFI_PHY_STANDARD_80211a;
  std::string phyModeA = "OfdmRate54Mbps";

  // WiFi standard B
  enum WifiPhyStandard wifiStandardB = WIFI_PHY_STANDARD_80211b;
  std::string phyModeB = "DsssRate11Mbps";

  // WiFi standard G
  enum WifiPhyStandard wifiStandardG = WIFI_PHY_STANDARD_80211g;
  std::string phyModeG = "ErpOfdmRate54Mbps";

  // WiFi SSID
  std::string ssidFirstWifi = "wifi-ssid-first";
  std::string ssidSecondWifi = "wifi-ssid-second";

  // Log Distance Propagation Loss Model exponent for WiFi link
  double logDistanceExponent1 = 1.0;
  double logDistanceExponent2 = 2.0;
  double logDistanceExponent3 = 3.0;



  // 10) prfix for voicemail calls
  std::string prefix = "/voicemail";



  // 11) variables for consumer and producer application
  //std::string noOfInterestsPerSec = "50";
  //std::string sizeOfDataPackets = "164";
  std::string noOfInterestsPerSec = "100";
  std::string sizeOfDataPackets = "82";

  // simulation time of 5 minutes in milliseconds (5 * 60 * 1000)
  uint32_t simTime = 5 * 60* 1000;

  // the average call duration for a phone call is 2,5 minutes (2.5 * 60 * 1000 = 150000):
  // http://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/DE/2011/110728DauerHandygespraeche.html
  // so the average voicemail duration can be smaller than the average call duration
  // the duration is beteween 0.5 minutes (0.5 * 60 * 1000 = 30000) and 1 minute (1* 60 * 1000 = 60000)
  uint32_t minVoicemailDuration = 30000;
  uint32_t maxVoicemailDuration = 60000;

  int callLength[numberOfClients];
  int callStartingTime[numberOfClients];
  int callStoppingTime[numberOfClients];



  // 12) variables for trace files
  // simulation time for trace files in seconds
  double simTimeForTrace = (double) (simTime/1000.0) - 0.00001;
  NodeContainer allClientNodes;






  /**
   * 1) parse BRITE config and generate a random network with BRITE (router nodes and connections between these nodes)
   */

  ns3::ndn::NetworkGenerator gen(confFile, queueNameGen, queueSize);

  // set variables for medium connectivity
  numberOfConnectionsInter = gen.getNumberOfAS(); // top level (#AS)
  numberOfConnectionsIntra = gen.getAllASNodesFromAS(0).size() / 2; // bottom level (#nodes in AS / 2)

  // add random connections between nodes, bandwidth in kbits and delay in ms
  gen.randomlyAddConnectionsBetweenTwoAS(numberOfConnectionsInter, minBWInter, maxBWInter, minDelayInter, maxDelayInter);
  gen.randomlyAddConnectionsBetweenTwoNodesPerAS(numberOfConnectionsIntra, minBWIntra, maxBWIntra, minDelayIntra, maxDelayIntra);






  /**
   * 2) insert fixed client nodes
   */

  gen.randomlyPlaceNodes(numberOfFixedClients, fixedClientName, ns3::ndn::NetworkGenerator::LeafNode, p2p);

  for (int i = 0; i < numberOfFixedClients; i++) {
    std::string clientName = fixedClientName + "_" + boost::lexical_cast<std::string>(i);

    Ptr<Node> client = Names::Find<Node>(clientName);
    fixedClientNodes.Add(client);
  }






  /**
   * 3) insert AP nodes
   */

  ns3::Ptr<ns3::UniformRandomVariable> randomAS = CreateObject<UniformRandomVariable>();
  int asId = randomAS->GetInteger(0, gen.getNumberOfAS()-1);

  // random AS for first WiFi (one AS)
  std::vector<int> asOfFirstWifi;
  asOfFirstWifi.push_back(asId);

  // random ASs for second WiFi (the other ASs)
  std::vector<int> asOfSecondWifi;
  for (int i = 0; i < gen.getNumberOfAS(); i++) {
    if (i != asId) {
      asOfSecondWifi.push_back(i);
    }
  }

  // insert all APs for the first WiFi
  gen.placeAPNodesAtPositionInAS(numberOfAPs, firstWifiAPs, routersOfFirstWifiAPs, ns3::ndn::NetworkGenerator::LeafNode, p2p, xPosFirstWifi, yPosFirstWifi, yPosNextAP, asOfFirstWifi);

  firstWifiAPNodes = gen.getCustomNodes(firstWifiAPs);
  routersOfFirstWifiAPNodes = gen.getCustomNodes(routersOfFirstWifiAPs);


  // insert all APs for the second WiFi
  gen.placeAPNodesAtPositionInAS(numberOfAPs, secondWifiAPs, routersOfSecondWifiAPs, ns3::ndn::NetworkGenerator::LeafNode, p2p, xPosSecondWifi, yPosSecondWifi, yPosNextAP, asOfSecondWifi);

  secondWifiAPNodes = gen.getCustomNodes(secondWifiAPs);
  routersOfSecondWifiAPNodes = gen.getCustomNodes(routersOfSecondWifiAPs);






  /**
   * 4) insert mobile client nodes
   */

  for (int i = 0; i < numberOfMobileClients; i++) {
    std::string clientName = mobileClientName + "_" + boost::lexical_cast<std::string>(i);

    gen.placeMobileClientNodeAtPos(clientName, mobileClientPosX, mobileClientPosY, mobileClientMinX, mobileClientMaxX, mobileClientMinY, mobileClientMaxY, mobileClientMobilityModel);

    Ptr<Node> client = Names::Find<Node>(clientName);
    mobileClientNodes.Add(client);
  }






  /**
   * 5) insert all links between all mobile client nodes and all AP nodes
   */
  
  for (int i = 0; i < numberOfMobileClients; i++) {

    for (int j = 0; j < firstWifiAPNodes.size(); j++) {
      gen.createWiFiLink(mobileClientNodes.Get (i), firstWifiAPNodes.Get(j), wifiStandardG, phyModeG, ssidFirstWifi, logDistanceExponent3);
    }

    for (int k = 0; k < secondWifiAPNodes.size(); k++) {
      gen.createWiFiLink(mobileClientNodes.Get (i), secondWifiAPNodes.Get(k), wifiStandardG, phyModeG, ssidSecondWifi, logDistanceExponent3);
    }

  }






  /**
   * 6) install NDN Stack on all nodes (router nodes, AP nodes, fixed client nodes and mobile client nodes)
   */
  ns3::ndn::StackHelper ndnHelper;
  //ndnHelper.SetOldContentStore ("ns3::ndn::cs::Stats::Lru","MaxSize", "1");
  ndnHelper.SetOldContentStore("ns3::ndn::cs::Nocache");
  ndnHelper.Install(gen.getAllASNodes());
  ndnHelper.Install(firstWifiAPNodes);
  ndnHelper.Install(secondWifiAPNodes);
  ndnHelper.Install(fixedClientNodes);
  ndnHelper.Install(mobileClientNodes);






  /**
   * 7) install routing helper on all nodes, this is needed that the tables are created at each node
   */
  ns3::ndn::GlobalRoutingHelper ndnGlobalRoutingHelper;
  ndnGlobalRoutingHelper.InstallAll();






  /**
   * 8) choosing forwarding strategy for all type of nodes (router nodes, AP nodes, fixed client nodes and mobile client nodes)
   */

  for (auto node : gen.getAllASNodes()) {
    ndn::StrategyChoiceHelper::Install(node, prefix, bestRouteForwardingStrategy);
  }

  for (auto node : firstWifiAPNodes) {
    ndn::StrategyChoiceHelper::Install(node, prefix, bestRouteForwardingStrategy);
  }

  for (auto node : secondWifiAPNodes) {
    ndn::StrategyChoiceHelper::Install(node, prefix, bestRouteForwardingStrategy);
  }

  for (auto node : fixedClientNodes) {
    ndn::StrategyChoiceHelper::Install(node, prefix, bestRouteForwardingStrategy);
  }

  for (int i = 0; i < numberOfMobileClients; i++) {
    std::string newPrefix = prefix + "_" + boost::lexical_cast<std::string>(i);
    ndn::StrategyChoiceHelper::Install(mobileClientNodes.Get(i), newPrefix, clientForwardingStrategy);
  }






  /**
   * 9) calculate call times for each pair of communication partners (mobile client with fixed client)
   */
  
  ns3::Ptr<ns3::UniformRandomVariable> randomCallLength = CreateObject<UniformRandomVariable>();
  ns3::Ptr<ns3::UniformRandomVariable> randomCallStartingTime = CreateObject<UniformRandomVariable>();

  // calculation of the voicemail duration, starttime and stoptime
  for (int i = 0; i < numberOfClients; i++) {

    // call length
    callLength[i] = randomCallLength->GetInteger(minVoicemailDuration, maxVoicemailDuration);

    // start call
    callStartingTime[i] = randomCallStartingTime->GetInteger(0, (simTime - callLength[i]));
    callStartingTime[i] = callStartingTime[i] / 1000;

    // stop call
    callStoppingTime[i] = callStartingTime[i] + (callLength[i] / 1000);

  }






  /**
   * 10) create consumer and producer applications (mobile clients are consumer, fixed clients are producer)
   */

  // install consumer
  for (int i = 0; i < numberOfMobileClients; i++) {
    std::string newPrefix = prefix + "_" + boost::lexical_cast<std::string>(i);

    ndn::AppHelper consumerHelper("ns3::ndn::ConsumerCbr");
    consumerHelper.SetPrefix(newPrefix);
    consumerHelper.SetAttribute("Frequency", StringValue(noOfInterestsPerSec));
    ApplicationContainer consumerContainer = consumerHelper.Install(mobileClientNodes.Get(i));
    consumerContainer.Start(Seconds(callStartingTime[i]));
    consumerContainer.Stop(Seconds(callStoppingTime[i]));
  }

  // install producer
  for (int i = 0; i < numberOfFixedClients; i++) {
    std::string newPrefix = prefix + "_" + boost::lexical_cast<std::string>(i);

    ndn::AppHelper producerHelper("ns3::ndn::Producer");
    producerHelper.SetPrefix(newPrefix);
    producerHelper.SetAttribute("PayloadSize", StringValue(sizeOfDataPackets));
    ApplicationContainer producerContainer = producerHelper.Install(fixedClientNodes.Get(i));
    producerContainer.Start(Seconds(callStartingTime[i]));
    producerContainer.Stop(Seconds(callStoppingTime[i]));

    // add prefix
    ndnGlobalRoutingHelper.AddOrigins(newPrefix, fixedClientNodes.Get(i));
  }






  /**
   * 11) calculate and install FIBs, all possible routes are calculated
   */

  ndnGlobalRoutingHelper.CalculateAllPossibleRoutes();






  /**
   * 12) remove specific routes from FIB
   */

  for (int i = 0; i < numberOfClients; i++) {
    std::string newPrefix = prefix + "_" + boost::lexical_cast<std::string>(i);

    // remove routes from all APs to all mobile clients
    for (int j = 0; j < numberOfAPs; j++) {
      ndn::FibHelper::RemoveRoutesToMobileClients(firstWifiAPNodes.Get(j), newPrefix);
      ndn::FibHelper::RemoveRoutesToMobileClients(secondWifiAPNodes.Get(j), newPrefix);
    }
  }


  // fill in and update router nodes which are connected to APs
  std::map<Ptr<Node>, int> routerNodesToAPs;
  for (int i = 0; i < numberOfAPs; i++) {
    addAndUpdateNodesToAPsMap(routerNodesToAPs, routersOfFirstWifiAPNodes.Get(i));
    addAndUpdateNodesToAPsMap(routerNodesToAPs, routersOfSecondWifiAPNodes.Get(i));
  }


  for (int i = 0; i < numberOfClients; i++) {
    std::string newPrefix = prefix + "_" + boost::lexical_cast<std::string>(i);

    // remove routes from all router nodes (which are connected to an AP node) to AP nodes
    for (auto nodes : routerNodesToAPs) {
      // RemoveRoutesToAPs: node, prefix, numberOfRoutes
      ndn::FibHelper::RemoveRoutesToAPs(nodes.first, newPrefix, nodes.second);
    }
  }






  /**
   * 13) Define Simulator stop
   */
  Simulator::Stop(MilliSeconds(simTime));






  /**
   * 14) create trace files for the evaluation later
   */

  // put all client nodes (fixed and mobile client nodes) for the trace files into a container
  for (auto node : mobileClientNodes) {
    allClientNodes.Add(node);
  }
  for (auto node : fixedClientNodes) {
    allClientNodes.Add(node);
  }

  // rate trace
  ndn::L3RateTracer::Install(allClientNodes, std::string(logDir + rateTraceFile), Seconds(simTimeForTrace));

  // app delay trace
  ndn::AppDelayTracer::Install(allClientNodes, std::string(logDir + appDelayTraceFile));






  /**
   * 15) create callLengths file for the evaluation later
   */

  ofstream file;
  file.open (logDir + callLengthFile);
  
  for (int i = 0; i < numberOfClients; i++) {
    file << Names::FindName(mobileClientNodes[i]) << "\t" << Names::FindName(fixedClientNodes[i]) << "\t" << callLength[i]/1000 << "\n";
  }
  file.close();






  /**
   * 16) Simulator run and destroy
   */

  Simulator::Run();
  Simulator::Destroy();

  return 0;

}

} // namespace ns3

int
main(int argc, char* argv[])
{
  return ns3::main(argc, argv);
}
