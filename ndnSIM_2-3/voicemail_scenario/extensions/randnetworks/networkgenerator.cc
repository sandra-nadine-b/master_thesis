#include "networkgenerator.h"
#include "ns3/double.h"

using namespace ns3;
using namespace ns3::ndn;

NS_LOG_COMPONENT_DEFINE ("NetworkGenerator");

NetworkGenerator::NetworkGenerator(std::string conf_file, std::string queueName, uint32_t queueSize)
{
  rvariable = CreateObject<UniformRandomVariable>();
  m_queueName = queueName;
  m_queueSize = queueSize;
  this->briteHelper = new NDNBriteHelper(conf_file, queueName, queueSize);
  briteHelper->BuildBriteTopology ();

  for(int i=0; i<getAllASNodes ().size (); i++)
  {
    Names::Add (std::string("Node_" + boost::lexical_cast<std::string>(i)), getAllASNodes ().Get (i));
  }
}

NetworkGenerator::NetworkGenerator(std::string conf_file, std::string seed_file, std::string newseed_file)
{
  rvariable = CreateObject<UniformRandomVariable>();
  this->briteHelper = new NDNBriteHelper(conf_file, seed_file, newseed_file);
  briteHelper->BuildBriteTopology ();

  for(int i=0; i<getAllASNodes ().size (); i++)
  {
    Names::Add (std::string("Node_" + boost::lexical_cast<std::string>(i)), getAllASNodes ().Get (i));
  }
  m_queueName = "";
  m_queueSize = 0;
}

void NetworkGenerator::randomlyPlaceNodes(int nodeCount, std::string setIdentifier, NodePlacement place, PointToPointHelper *p2p)
{
  std::vector<int> allAS;

  for(int i=0; i < getNumberOfAS (); i++)
    allAS.push_back (i);

  randomlyPlaceNodes(nodeCount,setIdentifier,place,p2p,allAS);
}

void NetworkGenerator::randomlyPlaceNodes (int nodeCount, std::string setIdentifier, NodePlacement place, PointToPointHelper *p2p, std::vector<int> ASnumbers)
{
  NodeContainer container;

  for(std::vector<int>::iterator it = ASnumbers.begin (); it != ASnumbers.end (); it++)
  {
    if(place == NetworkGenerator::ASNode)
    {
      container.Add (getAllASNodesFromAS(*it));
    }
    else
    {
      container.Add (getAllLeafNodesFromAS(*it));
    }
  }

  if(container.size () == 0)
  {
    NS_LOG_UNCOND("Could not place nodes, as no nodes are provided by the topology.");
    return;
  }

  NodeContainer customNodes;
  customNodes.Create (nodeCount);

  for(int i=0; i<customNodes.size (); i++)
  {
    Names::Add (std::string(setIdentifier + "_" + boost::lexical_cast<std::string>(i)), customNodes.Get (i));

    int rand = rvariable->GetInteger (0,container.size ()-1);
    p2p->Install (customNodes.Get (i), container.Get (rand));
  }
  nodeContainerMap[setIdentifier] = customNodes;
}

void NetworkGenerator::placeAPNodesAtPositionInAS(int nodeCount, std::string setIdentifierAP, std::string setIdentifierRouter, NodePlacement place, PointToPointHelper *p2p, int positionX, int positionY, int nextPositionY, std::vector<int> ASnumbers)
{
  NodeContainer container;

  // get all possible router nodes for AP nodes
  for(std::vector<int>::iterator it = ASnumbers.begin(); it != ASnumbers.end(); it++) {
    if(place == NetworkGenerator::ASNode) {
      container.Add (getAllASNodesFromAS(*it));
    } else {
      container.Add (getAllLeafNodesFromAS(*it));
    }
  }

  if(container.size () == 0) {
    NS_LOG_UNCOND("Could not place nodes, as no nodes are provided by the topology.");
    return;
  }

  NodeContainer routerNodes;
  NodeContainer apNodes;
  apNodes.Create (nodeCount);

  int newPositionY = positionY;

  for(int i = 0; i < apNodes.size(); i++) {
    Names::Add(std::string(setIdentifierAP + "_" + boost::lexical_cast<std::string>(i)), apNodes.Get(i));

    // get a random router node for AP
    int randomRouterNode = rvariable->GetInteger(0,container.size()-1);
    p2p->Install(apNodes.Get(i), container.Get(randomRouterNode));
    routerNodes.Add(container.Get(randomRouterNode));

    // set position with mobility model
    ObjectFactory factoryMobilityModel;
    factoryMobilityModel.SetTypeId("ns3::ConstantPositionMobilityModel");
    Ptr<MobilityModel> mobilityModel = DynamicCast<MobilityModel>(factoryMobilityModel.Create());
    apNodes.Get(i)->AggregateObject(mobilityModel);
    mobilityModel->SetPosition(Vector(positionX, newPositionY, 0));

    newPositionY = newPositionY + nextPositionY;
  }

  nodeContainerMap[setIdentifierAP] = apNodes;
  nodeContainerMap[setIdentifierRouter] = routerNodes;
}

void NetworkGenerator::placeMobileClientNodeAtPos(std::string name, int positionX, int positionY, int minX, int maxX, int minY, int maxY, std::string mobilityModelId)
{
  uint32_t systemId = 0;

  // bounds for the moving area
  double minXPos = positionX + minX;
  double maxXPos = positionX + maxX;
  double minYPos = positionY + minY;
  double maxYPos = positionY + maxY;

  // node
  Ptr<Node> node = CreateObject<Node>(systemId);

  // mobility model
  ObjectFactory factoryMobilityModel;
  factoryMobilityModel.SetTypeId(mobilityModelId);


  if (mobilityModelId.std::string::compare("ns3::RandomWaypointMobilityModel") == 0) { // RandomWaypointMobilityModel

    // position allocator - set the minX, maxX, minY and maxY position for the movement
    ObjectFactory boundary;
    boundary.SetTypeId ("ns3::RandomRectanglePositionAllocator");
    std::string positionXString = "ns3::UniformRandomVariable[Min=" + std::to_string(minXPos) + "|Max=" + std::to_string(maxXPos) + "]";
    std::string positionYString = "ns3::UniformRandomVariable[Min=" + std::to_string(minYPos) + "|Max=" + std::to_string(maxYPos) + "]";
    boundary.Set ("X", StringValue(positionXString));
    boundary.Set ("Y", StringValue(positionYString));
    Ptr<PositionAllocator> movementBoundary = boundary.Create()->GetObject<PositionAllocator>();

    // speed - set the speed for the movement
    Ptr<UniformRandomVariable> speed = CreateObject<UniformRandomVariable>();
    speed->SetAttribute("Min", DoubleValue(5));
    speed->SetAttribute("Max", DoubleValue(10));

    // set position allocator
    factoryMobilityModel.Set("PositionAllocator", PointerValue(movementBoundary));

    // set speed
    factoryMobilityModel.Set("Speed", PointerValue(speed));

    // set mobility model and position
    Ptr<MobilityModel> mobilityModel = DynamicCast<MobilityModel>(factoryMobilityModel.Create());
    mobilityModel->SetPosition(Vector(positionX, positionY, 0));
    node->AggregateObject(mobilityModel);

  } else if (mobilityModelId.std::string::compare("ns3::GaussMarkovMobilityModel") == 0) {

    // set bounds - moving area
    factoryMobilityModel.Set("Bounds", BoxValue(Box (minXPos, maxXPos, minYPos, maxYPos, 0, 0)));

    // set timestep - change current direction and speed after moving for this time
    factoryMobilityModel.Set("TimeStep", TimeValue (Seconds(2.0)));

    // set alpha - a constant representing the tunable parameter in the gauss-markov model (the tunable alpha parameter determines the how much memory and randomness you want to model)
    //factoryMobilityModel.Set("Alpha", DoubleValue (0.85));
    factoryMobilityModel.Set("Alpha", DoubleValue (0.0));

    // set mean velocity (Geschwindigkeit) - random variable used to assign the average velocity
    factoryMobilityModel.Set("MeanVelocity", StringValue ("ns3::UniformRandomVariable[Min=5|Max=10]"));

    // set mean direction radians (Richtung)- random variable used to assign the average direction
    factoryMobilityModel.Set("MeanDirection", StringValue ("ns3::UniformRandomVariable[Min=0|Max=6.283185307]"));

    // set normal velocity (Geschwindigkeit) - gaussian random variable used to calculate the next velocity value
    factoryMobilityModel.Set("NormalVelocity", StringValue ("ns3::NormalRandomVariable[Mean=0.0|Variance=0.0|Bound=0.0]"));

    // set normal direction (Richtung) - gaussian random variable used to calculate the next direction value
    factoryMobilityModel.Set("NormalDirection", StringValue ("ns3::NormalRandomVariable[Mean=0.0|Variance=0.2|Bound=0.4]"));

    // set mobility model and position
    Ptr<MobilityModel> mobilityModel = DynamicCast<MobilityModel>(factoryMobilityModel.Create());
    mobilityModel->SetPosition(Vector(positionX, positionY, 0));
    node->AggregateObject(mobilityModel);


  } else { // ConstantPositionMobilityModel

    // set mobility model and position
    Ptr<MobilityModel> mobilityModel = DynamicCast<MobilityModel>(factoryMobilityModel.Create());
    mobilityModel->SetPosition(Vector(positionX, positionY, 0));
    node->AggregateObject(mobilityModel);

  }

  // add name
  Names::Add("", name, node);
}

void NetworkGenerator::createWiFiLink(Ptr<Node> client, Ptr<Node> ap, enum WifiPhyStandard wifiStandard, std::string phyMode, std::string wifiSsid, double logDistanceExponent)
{
  // wifi helper
  WifiHelper wifiHelper = WifiHelper::Default();
  wifiHelper.SetStandard(wifiStandard);
  wifiHelper.SetRemoteStationManager("ns3::ConstantRateWifiManager", "DataMode", StringValue(phyMode));

  // wifi channel helper
  YansWifiChannelHelper wifiChannelHelper;
  wifiChannelHelper.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel");
  wifiChannelHelper.AddPropagationLoss("ns3::LogDistancePropagationLossModel", "Exponent", DoubleValue(logDistanceExponent));

  // yans wifi phy helper
  YansWifiPhyHelper wifiPhyHelper = YansWifiPhyHelper::Default();
  wifiPhyHelper.SetChannel(wifiChannelHelper.Create());

  // ssid
  Ssid ssid = Ssid(wifiSsid);

  // Non-QoS upper mac
  NqosWifiMacHelper wifiMacHelper = NqosWifiMacHelper::Default();
  wifiMacHelper.SetType("ns3::StaWifiMac", "Ssid", SsidValue(ssid));
  NodeContainer clientContainer;
  clientContainer.Add(client);
  NetDeviceContainer clientDevices = wifiHelper.Install(wifiPhyHelper, wifiMacHelper, clientContainer);

  wifiMacHelper.SetType("ns3::ApWifiMac", "Ssid", SsidValue(ssid));
  NodeContainer apContainer;
  apContainer.Add(ap);
  NetDeviceContainer apDevices = wifiHelper.Install(wifiPhyHelper, wifiMacHelper, apContainer);
}

void NetworkGenerator::randomlyAddConnectionsBetweenAllAS(int numberOfConnectionsPerAsPair, int minBW_kbits, int maxBw_kbits, int minDelay_ms, int maxDelay_ms)
{
  PointToPointHelper p2p;

  for(int i = 0; i<getNumberOfAS (); i++)
  {
    int j = i+1;
    while(j < getNumberOfAS ())
    {
      for(int c = 0; c < numberOfConnectionsPerAsPair; c++)
      {
        std::string delay(boost::lexical_cast<std::string>(rvariable->GetValue (minDelay_ms,maxDelay_ms)));
        delay.append ("ms");

        std::string bw(boost::lexical_cast<std::string>(rvariable->GetValue (minBW_kbits,maxBw_kbits)));
        bw.append ("Kbps");

        p2p.SetDeviceAttribute ("DataRate", StringValue (bw));
        p2p.SetChannelAttribute ("Delay", StringValue (delay));

        NodeContainer container = getPairOfUnconnectedNodes(i, j);
        if(container.size () == 2)
          p2p.Install (container.Get (0), container.Get (1));
        else
          NS_LOG_UNCOND("Unable to add new Connections");
      }
      j++;
    }
  }
}

void NetworkGenerator::randomlyAddConnectionsBetweenTwoAS(int numberOfConnectionsPairs, int minBW_kbits, int maxBw_kbits, int minDelay_ms, int maxDelay_ms)
{
  if(getNumberOfAS() <= 1)
  {
    NS_LOG_UNCOND("Error, at least two AS have to exists to add Connections between ASs!");
    return;
  }

  PointToPointHelper p2p;

  for(int i = 0; i < numberOfConnectionsPairs; i++)
  {
    std::string delay(boost::lexical_cast<std::string>(rvariable->GetValue (minDelay_ms,maxDelay_ms)));
    delay.append ("ms");

    std::string bw(boost::lexical_cast<std::string>(rvariable->GetValue (minBW_kbits,maxBw_kbits)));
    bw.append ("Kbps");

    p2p.SetDeviceAttribute ("DataRate", StringValue (bw));
    p2p.SetChannelAttribute ("Delay", StringValue (delay));
    NetworkGenerator::setQueue(&p2p, m_queueName, m_queueSize);

    int number_as1 = rvariable->GetInteger (0,getNumberOfAS()-1);
    int number_as2 = number_as1;

    while(number_as2 == number_as1)
      number_as2 = rvariable->GetInteger (0,getNumberOfAS()-1);

    NodeContainer container = getPairOfUnconnectedNodes(number_as1, number_as2);
    if(container.size () == 2)
      p2p.Install (container.Get (0), container.Get (1));
    else
      NS_LOG_UNCOND("Unable to add new Connections");
  }
}

void NetworkGenerator::randomlyAddConnectionsBetweenTwoNodesPerAS(int numberOfConnectionsPerAs, int minBW_kbits, int maxBw_kbits, int minDelay_ms, int maxDelay_ms)
{
  PointToPointHelper p2p;

  for(int as = 0; as < getNumberOfAS (); as++)
  {
    for(int i = 0; i < numberOfConnectionsPerAs; i++)
    {
      std::string delay(boost::lexical_cast<std::string>(rvariable->GetValue (minDelay_ms,maxDelay_ms)));
      delay.append ("ms");

      std::string bw(boost::lexical_cast<std::string>(rvariable->GetValue (minBW_kbits,maxBw_kbits)));
      bw.append ("Kbps");

      p2p.SetDeviceAttribute ("DataRate", StringValue (bw));
      p2p.SetChannelAttribute ("Delay", StringValue (delay));
      NetworkGenerator::setQueue(&p2p, m_queueName, m_queueSize);

      NodeContainer container = getPairOfUnconnectedNodes(as, as);
      if(container.size () == 2)
        p2p.Install (container.Get (0), container.Get (1));
      else
        NS_LOG_UNCOND("Unable to add new Connections");
    }
  }
}

int NetworkGenerator::getNumberOfAS ()
{
  return briteHelper->GetNAs ();
}

int NetworkGenerator::getNumberOfNodesInAS (int ASnumber)
{
  if(getNumberOfAS () < ASnumber)
  {
    return briteHelper->GetNNodesForAs (ASnumber);
  }
  return 0;
}

NodeContainer NetworkGenerator::getAllASNodes()
{
  NodeContainer container;

  for(int as=0; as < getNumberOfAS (); as++)
  {
    container.Add (getAllASNodesFromAS(as));
  }
  return container;
}

NodeContainer NetworkGenerator::getAllASNodesFromAS(int ASnumber)
{
  NodeContainer container;

  if(getNumberOfAS () < ASnumber)
    return container;

  for(int node=0; node < briteHelper->GetNNodesForAs(ASnumber); node++)
  {
    container.Add (briteHelper->GetNodeForAs (ASnumber,node));
  }

  return container;
}

NodeContainer NetworkGenerator::getAllLeafNodes()
{
  NodeContainer container;

  for(int as=0; as < getNumberOfAS (); as++)
  {
    container.Add (getAllLeafNodesFromAS(as));
  }

  return container;
}

NodeContainer NetworkGenerator::getAllLeafNodesFromAS(int ASnumber)
{
  NodeContainer container;

  if(getNumberOfAS () < ASnumber)
    return container;

  for(int node=0; node < briteHelper->GetNLeafNodesForAs (ASnumber); node++)
  {
    container.Add (briteHelper->GetLeafNodeForAs(ASnumber,node));
  }
  return container;
}

NodeContainer NetworkGenerator::getCustomNodes(std::string setIdentifier)
{
  return nodeContainerMap[setIdentifier];
}

void NetworkGenerator::creatRandomLinkFailure(double minTimestamp, double maxTimestamp, double minDuration, double maxDuration)
{
  creatRandomLinkFailure(minTimestamp, maxTimestamp, minDuration, maxDuration, 1.0, 1.0);
}

void NetworkGenerator::creatRandomLinkFailure(double minTimestamp, double maxTimestamp, double minDuration, double maxDuration,
                                              double minErrorRate, double maxErrorRate)
{
  int rand = rvariable->GetInteger(0,getNumberOfAS() - 1);

  NodeContainer c = getAllASNodesFromAS(rand);
  rand = rvariable->GetInteger (0, c.size ()-1);

  Ptr<Node> node = c.Get (rand);

  rand = rvariable->GetInteger (0,node->GetNDevices ()-1);
  Ptr<Channel> channel = node->GetDevice (rand)->GetChannel ();

  NodeContainer channelNodes;

  for(int i = 0; i < channel->GetNDevices (); i++)
  {
    Ptr<NetDevice> dev = channel->GetDevice (i);
    channelNodes.Add (dev->GetNode ());
  }

  if(channelNodes.size () != 2)
    NS_LOG_ERROR("Invalid Channel with more than 2 nodes...");
  else
  {
    double startTime = rvariable->GetValue (minTimestamp, maxTimestamp);
    double stopTime = startTime + rvariable->GetValue (minDuration, maxDuration);

    double errorRate = rvariable->GetValue(minErrorRate, maxErrorRate);

    //std::cout << "Fail Link between " << channelNodes.Get(0)->GetId() << " and " << channelNodes.Get (1)->GetId() << " from " << startTime << " to " << stopTime << std::endl;
    std::stringstream loggingInfo;
    loggingInfo << channelNodes.Get(0)->GetId() << "\t" << channelNodes.Get(1)->GetId() << "\t" << startTime << "\t" << stopTime << "\t" << errorRate;
    m_linkFailures.push_back(loggingInfo.str());

    // todo: add error rate
    Simulator::Schedule (MilliSeconds (startTime), ns3::ndn::LinkControlHelper::FailLink, channelNodes.Get (0), channelNodes.Get (1), errorRate);
    Simulator::Schedule (MilliSeconds (stopTime), ns3::ndn::LinkControlHelper::UpLink,   channelNodes.Get (0), channelNodes.Get (1));

    //fprintf(stderr, "Start LinkFail between %s and %s: %f\n",Names::FindName (channelNodes.Get (0)).c_str (),Names::FindName (channelNodes.Get (1)).c_str (), startTime);
    //fprintf(stderr, "Stop LinkFail between %s and %s: %f\n\n",Names::FindName (channelNodes.Get (0)).c_str (),Names::FindName (channelNodes.Get (1)).c_str (),stopTime);
  }
}

void
NetworkGenerator::setQueue(PointToPointHelper* p2p, std::string queueName, uint32_t queueSize)
{
  if (!queueName.empty()) {
    if (queueName.compare("DropTail_Packets") == 0) {
      p2p->SetQueue("ns3::DropTailQueue", 
        "Mode", StringValue("QUEUE_MODE_PACKETS"),
        "MaxPackets", StringValue(boost::lexical_cast<std::string>(queueSize)));

    } else if (queueName.compare("DropTail_Bytes") == 0) {
      p2p->SetQueue("ns3::DropTailQueue", 
        "Mode", StringValue("QUEUE_MODE_BYTES"),
        "MaxBytes", StringValue(boost::lexical_cast<std::string>(queueSize * 1000)));

    } else if (queueName.compare("Fair_Packets") == 0) {
      p2p->SetQueue("ns3::FairQueue", 
        "Mode", StringValue("QUEUE_MODE_PACKETS"),
        "MaxPackets", StringValue(boost::lexical_cast<std::string>(queueSize)));

    } else if (queueName.compare("Fair_Bytes") == 0) {
      p2p->SetQueue("ns3::FairQueue", 
        "Mode", StringValue("QUEUE_MODE_BYTES"),
        "MaxBytes", StringValue(boost::lexical_cast<std::string>(queueSize * 1000)));

    } else if (queueName.compare("PriorityQueue_Bytes") == 0) {
      p2p->SetQueue("ns3::PriorityQueue", 
        "Mode", StringValue("QUEUE_MODE_BYTES"),
        "MaxBytes", StringValue(boost::lexical_cast<std::string>(queueSize * 1000)));

    } else if (queueName.compare("PriorityQueue_Packets") == 0) {
      p2p->SetQueue("ns3::PriorityQueue", 
        "Mode", StringValue("QUEUE_MODE_PACKETS"),
        "MaxBytes", StringValue(boost::lexical_cast<std::string>(queueSize)));

    } else if (queueName.compare("WFQ") == 0) {
      p2p->SetQueue("ns3::WFQ", 
        "Mode", StringValue("QUEUE_MODE_BYTES"),
        "MaxBytes", StringValue(boost::lexical_cast<std::string>(queueSize * 1000)));

    } else if (queueName.compare("REDQueue_Bytes") == 0) {
      p2p->SetQueue("ns3::RedQueue", 
        "Mode", StringValue("QUEUE_MODE_BYTES"),
        "QueueLimit", StringValue(boost::lexical_cast<std::string>(queueSize * 1000)));

    } else if (queueName.compare("REDQueue_Packets") == 0) {
      p2p->SetQueue("ns3::RedQueue", 
        "Mode", StringValue("QUEUE_MODE_PACKETS"),
        "QueueLimit", StringValue(boost::lexical_cast<std::string>(queueSize)));
    } else {
      std::cout << "Invalid Queue Name selected (NetworkGenerator)" << std::endl;
      exit(-1);
    }
  }
}

bool NetworkGenerator::nodesConnected(Ptr<Node> n1, Ptr<Node> n2)
{
  int n1_nr_dev = n1->GetNDevices ();

  for(int i = 0; i < n1_nr_dev; i++)
  {
    Ptr<NetDevice> dev = n1->GetDevice (i);
    Ptr<Channel> channel = dev->GetChannel ();
    int channel_nr_dev = channel->GetNDevices ();

    for(int j = 0; j < channel_nr_dev; j++)
    {
      Ptr<Node> con_node = channel->GetDevice (j)->GetNode ();
      if(n2->GetId () == con_node->GetId ())
        return true;
    }
  }
  return false;
}

bool NetworkGenerator::nodesConnected(Ptr<Node> n1, Ptr<Node> n2, int& n1_dev_id, int& n2_dev_id)
{
  int n1_nr_dev = n1->GetNDevices ();

  for(int i = 0; i < n1_nr_dev; i++)
  {
    Ptr<NetDevice> dev = n1->GetDevice (i);
    Ptr<Channel> channel = dev->GetChannel ();
    int channel_nr_dev = channel->GetNDevices ();

    for(int j = 0; j < channel_nr_dev; j++)
    {
      Ptr<Node> con_node = channel->GetDevice (j)->GetNode ();
      if(n2->GetId () == con_node->GetId ())
      {
        n1_dev_id = i;
        n2_dev_id = j;
        return true;
      }
    }
  }
  return false;
}

NodeContainer NetworkGenerator::getPairOfUnconnectedNodes(int as1, int as2)
{
  NodeContainer as1_nodes = getAllASNodesFromAS (as1);
  NodeContainer as2_nodes = getAllASNodesFromAS (as2);

  while(as1_nodes.size () > 0)
  {
    int rand_node_1 = rvariable->GetInteger (0,as1_nodes.size ()-1);
    Ptr<Node> as1_node = as1_nodes.Get (rand_node_1);
    as1_nodes = removeNode (as1_nodes, as1_node);

    NodeContainer as2_nodes_cp = as2_nodes;
    while(as2_nodes_cp.size () > 0)
    {
      int rand_node_2 = rvariable->GetInteger (0,as2_nodes_cp.size ()-1);
      Ptr<Node> as2_node = as2_nodes_cp.Get (rand_node_2);
      as2_nodes_cp = removeNode (as2_nodes_cp, as2_node);

      if(as1_node->GetId () != as2_node->GetId () &&
         !nodesConnected(as1_node, as2_node))
      {
        NodeContainer c;
        c.Add (as1_node);
        c.Add (as2_node);
        return c;
      }
    }
  }
  return NodeContainer();
}

NodeContainer NetworkGenerator::removeNode(NodeContainer container, Ptr<Node> node)
{
  NodeContainer result;
  for(NodeContainer::iterator it = container.begin (); it!=container.end (); ++it)
  {
    if( (*it)->GetId() != node->GetId ())
      result.Add (*it);
  }
  return result;
}

double NetworkGenerator::calculateConnectivity ()
{
  NodeContainer allNodes;
  allNodes.Add (getAllASNodes ());

  Ptr<Node> n;
  double connectivity = 0.0;

  for(int i = 0; i < allNodes.size (); i++)
  {
    n = allNodes.Get (i);
    connectivity += n->GetNDevices (); // degree summation
  }

  connectivity /= allNodes.size ();
  connectivity /= (allNodes.size () - 1);

  return connectivity;
}

void NetworkGenerator::exportTopology(std::string fname, string server_identifier, string client_identifier)
{
  ofstream file;
  file.open (fname.c_str (),ios::out);

  //first extract all nodes / edges

  ns3::NodeContainer nodes = getAllASNodes ();
  nodes.Add (getCustomNodes(server_identifier));
  nodes.Add (getCustomNodes(client_identifier));

  //print heading
  file << "#number of nodes\n" << boost::lexical_cast<std::string>(nodes.size ()) << "\n";

  //print heading
  file << "#nodes (n1,n2,bandwidth in bits)\n";

  for(NodeContainer::iterator n1 = nodes.begin (); n1!=nodes.end ();++n1)
  {
    for(NodeContainer::iterator n2 = n1+1; n2!=nodes.end (); ++n2)
    {
      /*if((*n1)->GetId() == (*n2)->GetId())
        continue;*/

      if(nodesConnected(*n1,*n2))
      {
        //fprintf(stderr,"%d connected with %d\n", (*n1)->GetId(),(*n2)->GetId());
        file << "(" << boost::lexical_cast<std::string>((*n1)->GetId()) << ","
                    << boost::lexical_cast<std::string>((*n2)->GetId()) << ","
                    << boost::lexical_cast<std::string>(getBandwidth (*n1,*n2)) << ")\n";
      }
    }
  }
  file << "#eof";
  file.close ();
}

void 
NetworkGenerator::exportLinkFailures(std::string fname)
{
  ofstream file;
  file.open (fname.c_str(), ios::out);

  file << "First_Node_ID" << "\t" << "Second_Node_ID" << "\t" << "start" << "\t" << "end" << "\n";

  for (auto iterator = m_linkFailures.begin(); iterator != m_linkFailures.end(); ++iterator) {
    file << *iterator << "\n";
  }

  file.close();
}

void NetworkGenerator::exportCoreNetworkWithFaceInformation(std::string fname)
{
  ofstream file;
  file.open (fname.c_str (),ios::out);

  //first extract all nodes / edges
  ns3::NodeContainer nodes = getAllASNodes ();

  //print heading
  file << "#number of nodes\n" << boost::lexical_cast<std::string>(nodes.size ()) << "\n";

  //print heading
  file << "#nodes (n1,n1_faceId,n2,n2_faceId,bandwidth in bits)\n";

  for(NodeContainer::iterator n1 = nodes.begin (); n1!=nodes.end ();++n1)
  {
    for(NodeContainer::iterator n2 = n1+1; n2!=nodes.end (); ++n2)
    {
      int n1_dev_id = INT_MIN;
      int n2_dev_id = INT_MIN;

      if(nodesConnected(*n1,*n2, n1_dev_id, n2_dev_id))
      {
        //fprintf(stderr,"%d connected with %d\n", (*n1)->GetId(),(*n2)->GetId());
        file << "(" << boost::lexical_cast<std::string>((*n1)->GetId()) << ","
                    << boost::lexical_cast<std::string>(n1_dev_id+256) << "," // +256
                    << boost::lexical_cast<std::string>((*n2)->GetId()) << ","
                    << boost::lexical_cast<std::string>(n2_dev_id+256) << "," // +256
                    << boost::lexical_cast<std::string>(getBandwidth (*n1,*n2)) << ")\n";
      }
    }
  }

  file << "#eof";
  file.close ();
}

uint64_t NetworkGenerator::getBandwidth(Ptr<Node> n1, Ptr<Node> n2)
{
  int n1_nr_dev = n1->GetNDevices ();

  for(int i = 0; i < n1_nr_dev; i++)
  {
    Ptr<NetDevice> dev = n1->GetDevice (i);
    Ptr<Channel> channel = dev->GetChannel ();
    int channel_nr_dev = channel->GetNDevices ();

    for(int j = 0; j < channel_nr_dev; j++)
    {
      Ptr<Node> con_node = channel->GetDevice (j)->GetNode ();
      if(n2->GetId () == con_node->GetId ())
      {
        ns3::Ptr<ns3::PointToPointNetDevice> nd1 = dev->GetObject<ns3::PointToPointNetDevice>();
        ns3::DataRateValue dv;
        nd1->GetAttribute("DataRate", dv);
        return dv.Get().GetBitRate();
      }
    }
  }
  return 0;
}

void NetworkGenerator::introduceError (double min_error_rate, double max_error_rate)
{

  if(min_error_rate == 0.0 && max_error_rate == 0.0 || min_error_rate > max_error_rate)
    return;

  NodeContainer c = getAllASNodes ();

  for(int i = 0; i < c.size (); i++)
  {
    Ptr<Node> n = c.Get (i);
    for(int k = 0; k < n->GetNDevices (); k++)
    {
      //creates error model between
      Ptr<RateErrorModel> em = CreateObject<RateErrorModel> ();
      em->SetAttribute ("ErrorRate", DoubleValue (rvariable->GetValue (min_error_rate, max_error_rate)));

      Ptr<NetDevice> dev = n->GetDevice (k);
      dev->SetAttribute ("ReceiveErrorModel", PointerValue (em));

    }
  }

}
