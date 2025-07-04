import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styled from 'styled-components';

const Container = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
`;

const Header = styled.header`
  text-align: center;
  padding: 2rem;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
`;

const Title = styled.h1`
  font-size: 3rem;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  margin: 0.5rem 0;
  opacity: 0.9;
`;

const Dashboard = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const Card = styled.div`
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  padding: 1.5rem;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
`;

const CardTitle = styled.h3`
  margin: 0 0 1rem 0;
  font-size: 1.5rem;
  text-align: center;
`;

const Metric = styled.div`
  text-align: center;
  margin: 1rem 0;
`;

const MetricValue = styled.div`
  font-size: 3rem;
  font-weight: bold;
  color: ${props => props.color || '#fff'};
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
`;

const MetricLabel = styled.div`
  font-size: 1rem;
  opacity: 0.8;
  margin-top: 0.5rem;
`;

const StatusIndicator = styled.div`
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  background: ${props => props.status === 'healthy' ? '#4CAF50' : '#F44336'};
  color: white;
  font-weight: bold;
  margin: 0.5rem;
`;

const UploadSection = styled.div`
  text-align: center;
  padding: 1rem;
`;

const FileInput = styled.input`
  margin: 1rem;
  padding: 0.5rem;
  border: none;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  &::file-selector-button {
    background: rgba(255, 255, 255, 0.3);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
  }
`;

const Button = styled.button`
  background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  margin: 0.5rem;
  transition: transform 0.2s;
  
  &:hover {
    transform: translateY(-2px);
  }
  
  &:active {
    transform: translateY(0);
  }
`;

const AgentList = styled.div`
  max-height: 300px;
  overflow-y: auto;
`;

const Agent = styled.div`
  background: rgba(255, 255, 255, 0.1);
  margin: 0.5rem 0;
  padding: 0.75rem;
  border-radius: 10px;
  border-left: 4px solid #4ECDC4;
`;

function App() {
  const [stats, setStats] = useState({});
  const [agents, setAgents] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState('Loading...');

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  useEffect(() => {
    fetchStats();
    fetchAgents();
    const interval = setInterval(() => {
      fetchStats();
      fetchAgents();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/dashboard/stats`);
      setStats(response.data);
      setStatus('Connected');
    } catch (error) {
      setStatus('Disconnected');
      console.error('Error fetching stats:', error);
    }
  };

  const fetchAgents = async () => {
    try {
      const response = await axios.get(`${API_URL}/agents`);
      setAgents(response.data.agents || []);
    } catch (error) {
      console.error('Error fetching agents:', error);
    }
  };

  const handleFileUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('type', 'image');

    try {
      await axios.post(`${API_URL}/media`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setSelectedFile(null);
      fetchStats();
      alert('Cat photo uploaded successfully! 🐱');
    } catch (error) {
      alert('Error uploading file: ' + error.message);
    }
  };

  const initializeAgents = async () => {
    try {
      await axios.post(`${API_URL}/agents/initialize`);
      fetchAgents();
      alert('Agents initialized successfully! 🐾');
    } catch (error) {
      alert('Error initializing agents: ' + error.message);
    }
  };

  const startSimulation = async () => {
    try {
      await axios.post(`${API_URL}/simulation/start`);
      fetchStats();
      alert('Simulation started! 🚀');
    } catch (error) {
      alert('Error starting simulation: ' + error.message);
    }
  };

  const pauseSimulation = async () => {
    try {
      await axios.post(`${API_URL}/simulation/pause`);
      fetchStats();
      alert('Simulation paused! ⏸️');
    } catch (error) {
      alert('Error pausing simulation: ' + error.message);
    }
  };

  const getHappinessColor = (happiness) => {
    if (happiness >= 0.8) return '#4CAF50';
    if (happiness >= 0.6) return '#FF9800';
    return '#F44336';
  };

  return (
    <Container>
      <Header>
        <Title>🐱 CHAOSTOWN 🏰</Title>
        <Subtitle>Cat-Centric AI Civilization Dashboard</Subtitle>
        <StatusIndicator status={status === 'Connected' ? 'healthy' : 'error'}>
          {status}
        </StatusIndicator>
      </Header>

      <Dashboard>
        <Card>
          <CardTitle>😻 Cat Happiness</CardTitle>
          <Metric>
            <MetricValue color={getHappinessColor(stats.cat_happiness)}>
              {((stats.cat_happiness || 0) * 100).toFixed(1)}%
            </MetricValue>
            <MetricLabel>
              {stats.cat_happiness >= 0.8 ? 'Excellent!' : 'Needs Attention!'}
            </MetricLabel>
          </Metric>
        </Card>

        <Card>
          <CardTitle>🤖 Active Agents</CardTitle>
          <Metric>
            <MetricValue color="#4ECDC4">
              {stats.agent_count || 0}
            </MetricValue>
            <MetricLabel>Digital Citizens</MetricLabel>
          </Metric>
        </Card>

        <Card>
          <CardTitle>🎮 Simulation</CardTitle>
          <Metric>
            <StatusIndicator status={stats.simulation_running ? 'healthy' : 'error'}>
              {stats.simulation_running ? 'Running' : 'Paused'}
            </StatusIndicator>
            <div>
              <Button onClick={startSimulation}>Start</Button>
              <Button onClick={pauseSimulation}>Pause</Button>
            </div>
          </Metric>
        </Card>

        <Card>
          <CardTitle>📸 Upload Cat Media</CardTitle>
          <UploadSection>
            <div>Boost happiness by uploading cat photos!</div>
            <FileInput
              type="file"
              accept="image/*"
              onChange={(e) => setSelectedFile(e.target.files[0])}
            />
            <div>
              <Button onClick={handleFileUpload} disabled={!selectedFile}>
                Upload Photo 📷
              </Button>
            </div>
          </UploadSection>
        </Card>

        <Card>
          <CardTitle>🐾 Agent Control</CardTitle>
          <Metric>
            <Button onClick={initializeAgents}>
              Initialize Agents
            </Button>
            <MetricLabel>
              Creates 10 cat citizens
            </MetricLabel>
          </Metric>
        </Card>

        <Card>
          <CardTitle>👥 Agent Population</CardTitle>
          <AgentList>
            {agents.length > 0 ? (
              agents.map(agent => (
                <Agent key={agent.id}>
                  <div><strong>{agent.name}</strong></div>
                  <div>Type: {agent.type}</div>
                  <div>Happiness: {(agent.happiness * 100).toFixed(0)}%</div>
                  <div>Energy: {(agent.energy * 100).toFixed(0)}%</div>
                </Agent>
              ))
            ) : (
              <div>No agents initialized yet</div>
            )}
          </AgentList>
        </Card>
      </Dashboard>
    </Container>
  );
}

export default App;