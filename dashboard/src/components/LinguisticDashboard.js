import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import useWebSocket from '../hooks/useWebSocket';
import RealTimeLinguisticMetrics from './RealTimeLinguisticMetrics';

const LinguisticContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
`;

const LinguisticCard = styled.div`
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  min-height: 300px;
`;

const CardTitle = styled.h3`
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
  text-align: center;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
`;

const LiveFeed = styled.div`
  height: 250px;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
  font-family: 'Courier New', monospace;
`;

const DotPattern = styled.div`
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 0.75rem;
  margin: 0.5rem 0;
  border-left: 4px solid ${props => props.isInnovation ? '#FFD700' : '#4ECDC4'};
  animation: ${props => props.isNew ? 'fadeIn 0.5s ease-in' : 'none'};
  
  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
  }
`;

const PatternMeta = styled.div`
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const PatternContent = styled.div`
  font-size: 1.2rem;
  font-weight: bold;
  letter-spacing: 0.1em;
  line-height: 1.4;
  color: #fff;
  white-space: pre-line;
  text-align: center;
  background: rgba(0, 0, 0, 0.3);
  padding: 0.5rem;
  border-radius: 5px;
  min-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const ComplexityBadge = styled.span`
  background: ${props => {
    if (props.complexity < 0.3) return '#4CAF50';
    if (props.complexity < 0.6) return '#FF9800';
    return '#F44336';
  }};
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: bold;
`;

const InnovationBadge = styled.span`
  background: linear-gradient(45deg, #FFD700, #FFA000);
  color: #000;
  padding: 0.2rem 0.5rem;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: bold;
  animation: pulse 2s infinite;
  
  @keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(255, 215, 0, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 215, 0, 0); }
  }
`;

const MetricGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
`;

const MetricBox = styled.div`
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: 10px;
`;

const MetricValue = styled.div`
  font-size: 1.8rem;
  font-weight: bold;
  color: ${props => props.color || '#4ECDC4'};
  margin-bottom: 0.3rem;
`;

const MetricLabel = styled.div`
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.8);
`;

const AgentRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  margin: 0.5rem 0;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  border-left: 4px solid ${props => {
    if (props.stage >= 4) return '#FFD700';
    if (props.stage >= 3) return '#4CAF50';
    if (props.stage >= 2) return '#FF9800';
    return '#9E9E9E';
  }};
`;

const StageIndicator = styled.div`
  background: ${props => {
    if (props.stage >= 4) return 'linear-gradient(45deg, #FFD700, #FFA000)';
    if (props.stage >= 3) return 'linear-gradient(45deg, #4CAF50, #45A049)';
    if (props.stage >= 2) return 'linear-gradient(45deg, #FF9800, #F57C00)';
    return 'linear-gradient(45deg, #9E9E9E, #757575)';
  }};
  color: ${props => props.stage >= 2 ? '#000' : '#fff'};
  padding: 0.3rem 0.6rem;
  border-radius: 15px;
  font-size: 0.7rem;
  font-weight: bold;
  min-width: 60px;
  text-align: center;
`;

const ConnectionStatus = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  justify-content: center;
`;

const StatusDot = styled.div`
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: ${props => props.connected ? '#4CAF50' : '#F44336'};
  animation: ${props => props.connected ? 'pulse 2s infinite' : 'none'};
  
  @keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.2); opacity: 0.7; }
    100% { transform: scale(1); opacity: 1; }
  }
`;

const RSSForm = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const TextArea = styled.textarea`
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  padding: 1rem;
  color: #fff;
  resize: vertical;
  min-height: 100px;
  font-family: inherit;
  
  &::placeholder {
    color: rgba(255, 255, 255, 0.6);
  }
  
  &:focus {
    outline: none;
    border-color: #4ECDC4;
    box-shadow: 0 0 10px rgba(78, 205, 196, 0.3);
  }
`;

const SubmitButton = styled.button`
  background: linear-gradient(45deg, #4ECDC4, #44A08D);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.2s;
  
  &:hover {
    transform: translateY(-2px);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }
`;

const STAGE_NAMES = {
  1: "Primal",
  2: "Emotional", 
  3: "Conceptual",
  4: "Cultural",
  5: "Meta-linguistic"
};

const COLORS = ['#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F'];

function LinguisticDashboard() {
  const [communications, setCommunications] = useState([]);
  const [agents, setAgents] = useState([]);
  const [complexityData, setComplexityData] = useState([]);
  const [stageDistribution, setStageDistribution] = useState([]);
  const [rssContent, setRssContent] = useState('');
  const [submitting, setSubmitting] = useState(false);
  
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  const WS_URL = API_URL.replace('http://', 'ws://').replace('https://', 'wss://');

  // WebSocket connection for live communications
  const { isConnected: wsConnected, lastMessage } = useWebSocket(
    `${WS_URL}/api/linguistic/ws/linguistic/live`,
    {
      onMessage: (data) => {
        if (data.event_type === 'communication') {
          handleNewCommunication(data);
        } else if (data.event_type === 'stage_advancement') {
          fetchAgents();
        }
      },
      reconnectAttempts: 10,
      reconnectInterval: 3000
    }
  );

  // Fetch initial data on component mount
  useEffect(() => {
    fetchInitialData();
  }, []);

  const handleNewCommunication = (message) => {
    const newComm = {
      id: message.data.id,
      agent_id: message.data.agent_id,
      pattern: message.data.pattern,
      complexity: message.data.complexity,
      trigger: message.data.trigger,
      is_innovation: message.data.is_innovation,
      timestamp: new Date(message.timestamp),
      pressure: message.data.pressure,
      isNew: true
    };
    
    setCommunications(prev => {
      const updated = [newComm, ...prev.slice(0, 49)]; // Keep last 50
      return updated;
    });
    
    // Update complexity chart data
    setComplexityData(prev => {
      const newData = [...prev, {
        time: new Date().toLocaleTimeString(),
        complexity: message.data.complexity,
        timestamp: Date.now()
      }].slice(-20); // Keep last 20 points
      return newData;
    });
  };

  const fetchInitialData = async () => {
    await Promise.all([
      fetchAgents(),
      fetchRecentCommunications(),
      fetchStageDistribution()
    ]);
  };

  const fetchStageDistribution = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/linguistic/evolution/stage-distribution`);
      if (response.data.stage_distribution) {
        const stageData = Object.entries(response.data.stage_distribution).map(([stage, count]) => ({
          name: `Stage ${stage}: ${STAGE_NAMES[stage]}`,
          value: count,
          stage: parseInt(stage)
        }));
        setStageDistribution(stageData);
      }
    } catch (error) {
      console.error('Error fetching stage distribution:', error);
    }
  };

  const fetchAgents = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/linguistic/evolution/stage-distribution`);
      // This is a simplified endpoint, in production we'd get full agent details
      // For now, simulate some agent data
      const mockAgents = Array.from({length: response.data.total_agents || 0}, (_, i) => ({
        id: `agent_${i}`,
        name: `Agent ${i + 1}`,
        linguistic_stage: Math.floor(Math.random() * 5) + 1,
        vocabulary_size: Math.floor(Math.random() * 20) + 1,
        literacy_level: Math.random(),
        total_communications: Math.floor(Math.random() * 100)
      }));
      setAgents(mockAgents);
    } catch (error) {
      console.error('Error fetching agents:', error);
    }
  };

  const fetchRecentCommunications = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/linguistic/communications/recent?limit=20`);
      if (response.data.communications) {
        const formattedComms = response.data.communications.map(comm => ({
          ...comm,
          timestamp: new Date(comm.timestamp),
          isNew: false
        }));
        setCommunications(formattedComms);
      }
    } catch (error) {
      console.error('Error fetching communications:', error);
    }
  };

  const submitRSSFeed = async (e) => {
    e.preventDefault();
    if (!rssContent.trim()) return;
    
    setSubmitting(true);
    try {
      const agentIds = agents.slice(0, 5).map(a => a.id); // Submit to first 5 agents
      const response = await axios.post(`${API_URL}/api/linguistic/rss/feed`, {
        agent_ids: agentIds,
        feed_content: rssContent,
        feed_source: 'dashboard_input',
        quality_score: 1.0,
        batch_process: false
      });
      
      setRssContent('');
      alert(`RSS feed processed for ${response.data.processed_agents} agents!`);
    } catch (error) {
      alert('Error processing RSS feed: ' + error.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      {/* Real-time Metrics */}
      <RealTimeLinguisticMetrics />
      
      <LinguisticContainer>
        {/* Live Communication Feed */}
        <LinguisticCard>
          <CardTitle>
            🛸 Live Alien Communications
            <ConnectionStatus>
              <StatusDot connected={wsConnected} />
              {wsConnected ? 'Live' : 'Offline'}
            </ConnectionStatus>
          </CardTitle>
        <LiveFeed>
          {communications.length > 0 ? (
            communications.map((comm, index) => (
              <DotPattern 
                key={`${comm.id}_${index}`} 
                isInnovation={comm.is_innovation}
                isNew={comm.isNew}
              >
                <PatternMeta>
                  <span>Agent {comm.agent_id}</span>
                  <div>
                    <ComplexityBadge complexity={comm.complexity}>
                      {(comm.complexity * 100).toFixed(0)}%
                    </ComplexityBadge>
                    {comm.is_innovation && <InnovationBadge>NEW!</InnovationBadge>}
                  </div>
                </PatternMeta>
                <PatternContent>{comm.pattern}</PatternContent>
              </DotPattern>
            ))
          ) : (
            <div style={{textAlign: 'center', color: 'rgba(255,255,255,0.6)', marginTop: '2rem'}}>
              No alien communications yet...
              <br />
              <small>Waiting for agents to develop language</small>
            </div>
          )}
        </LiveFeed>
      </LinguisticCard>

      {/* Stage Distribution Chart */}
      <LinguisticCard>
        <CardTitle>📊 Linguistic Stage Distribution</CardTitle>
        {stageDistribution.length > 0 ? (
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={stageDistribution}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={100}
                dataKey="value"
                label={({ name, value }) => `${name}: ${value}`}
              >
                {stageDistribution.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        ) : (
          <div style={{textAlign: 'center', color: 'rgba(255,255,255,0.6)', marginTop: '2rem'}}>
            No agent stage data yet...
          </div>
        )}
      </LinguisticCard>

      {/* Complexity Evolution */}
      <LinguisticCard>
        <CardTitle>🧠 Complexity Evolution</CardTitle>
        <ResponsiveContainer width="100%" height={250}>
          <LineChart data={complexityData}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis 
              dataKey="time" 
              stroke="rgba(255,255,255,0.6)"
              fontSize={12}
            />
            <YAxis 
              stroke="rgba(255,255,255,0.6)"
              fontSize={12}
              domain={[0, 1]}
            />
            <Tooltip 
              contentStyle={{
                backgroundColor: 'rgba(0,0,0,0.8)',
                border: '1px solid rgba(255,255,255,0.3)',
                borderRadius: '8px'
              }}
            />
            <Line 
              type="monotone" 
              dataKey="complexity" 
              stroke="#4ECDC4" 
              strokeWidth={2}
              dot={{ fill: '#4ECDC4', strokeWidth: 2, r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </LinguisticCard>

      {/* Agent Development */}
      <LinguisticCard>
        <CardTitle>🤖 Agent Development</CardTitle>
        <div style={{maxHeight: '250px', overflowY: 'auto'}}>
          {agents.map(agent => (
            <AgentRow key={agent.id} stage={agent.linguistic_stage}>
              <div>
                <div style={{fontWeight: 'bold'}}>{agent.name}</div>
                <div style={{fontSize: '0.8rem', opacity: 0.8}}>
                  Vocab: {agent.vocabulary_size} | Comms: {agent.total_communications}
                </div>
              </div>
              <StageIndicator stage={agent.linguistic_stage}>
                Stage {agent.linguistic_stage}
              </StageIndicator>
            </AgentRow>
          ))}
        </div>
      </LinguisticCard>

      {/* RSS Feed Interface */}
      <LinguisticCard>
        <CardTitle>📚 RSS Feed Literacy Boost</CardTitle>
        <RSSForm onSubmit={submitRSSFeed}>
          <TextArea
            value={rssContent}
            onChange={(e) => setRssContent(e.target.value)}
            placeholder="Enter text content to boost agent literacy development...

Example:
- News articles
- Stories  
- Educational content
- Any text to help agents learn character recognition"
            maxLength={1000}
          />
          <SubmitButton type="submit" disabled={!rssContent.trim() || submitting}>
            {submitting ? 'Processing...' : 'Submit RSS Feed'}
          </SubmitButton>
        </RSSForm>
        <div style={{fontSize: '0.8rem', opacity: 0.7, marginTop: '0.5rem'}}>
          Agents will extract emotional vibes and gradually develop character recognition
        </div>
      </LinguisticCard>
    </LinguisticContainer>
  );
}

export default LinguisticDashboard;