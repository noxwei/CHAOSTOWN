import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import useWebSocket from '../hooks/useWebSocket';

const MetricsContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
`;

const MetricCard = styled.div`
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  }
`;

const MetricValue = styled.div`
  font-size: 2.5rem;
  font-weight: bold;
  color: ${props => props.color || '#4ECDC4'};
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  transition: all 0.5s ease;
`;

const MetricLabel = styled.div`
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
`;

const MetricChange = styled.div`
  font-size: 0.8rem;
  color: ${props => {
    if (props.change > 0) return '#4CAF50';
    if (props.change < 0) return '#F44336';
    return 'rgba(255, 255, 255, 0.6)';
  }};
  margin-top: 0.3rem;
  font-weight: bold;
`;

const ConnectionIndicator = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  padding: 0.5rem;
  border-radius: 20px;
  background: ${props => props.connected ? 
    'linear-gradient(45deg, #4CAF50, #45A049)' : 
    'linear-gradient(45deg, #F44336, #D32F2F)'
  };
  color: white;
  font-weight: bold;
  font-size: 0.9rem;
`;

const PulsingDot = styled.div`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: white;
  animation: ${props => props.connected ? 'pulse 2s infinite' : 'none'};
  
  @keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.3); opacity: 0.7; }
    100% { transform: scale(1); opacity: 1; }
  }
`;

const LiveBadge = styled.div`
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: linear-gradient(45deg, #FF4081, #E91E63);
  color: white;
  padding: 0.2rem 0.5rem;
  border-radius: 10px;
  font-size: 0.7rem;
  font-weight: bold;
  animation: glow 2s infinite;
  
  @keyframes glow {
    0%, 100% { box-shadow: 0 0 5px rgba(255, 64, 129, 0.5); }
    50% { box-shadow: 0 0 20px rgba(255, 64, 129, 0.8); }
  }
`;

function RealTimeLinguisticMetrics() {
  const [metrics, setMetrics] = useState({
    total_agents: 0,
    active_agents: 0,
    total_communications: 0,
    unique_patterns: 0,
    language_families: 0,
    average_complexity: 0,
    innovation_rate: 0,
    literacy_progression: 0
  });
  
  const [previousMetrics, setPreviousMetrics] = useState({});
  const [changes, setChanges] = useState({});

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  const WS_URL = API_URL.replace('http://', 'ws://').replace('https://', 'wss://');

  const { isConnected, lastMessage } = useWebSocket(
    `${WS_URL}/api/linguistic/ws/linguistic/metrics`,
    {
      onMessage: (data) => {
        if (data.event_type === 'metrics_update') {
          updateMetrics(data.data);
        }
      },
      onOpen: () => {
        console.log('Connected to metrics stream');
      },
      onClose: () => {
        console.log('Disconnected from metrics stream');
      },
      reconnectAttempts: 10,
      reconnectInterval: 3000
    }
  );

  const updateMetrics = (newMetrics) => {
    setPreviousMetrics(metrics);
    setMetrics(prev => ({ ...prev, ...newMetrics }));
    
    // Calculate changes
    const newChanges = {};
    Object.keys(newMetrics).forEach(key => {
      if (typeof newMetrics[key] === 'number' && typeof metrics[key] === 'number') {
        newChanges[key] = newMetrics[key] - metrics[key];
      }
    });
    setChanges(newChanges);
  };

  // Fetch initial metrics
  useEffect(() => {
    const fetchInitialMetrics = async () => {
      try {
        const response = await fetch(`${API_URL}/api/linguistic/evolution/metrics`);
        const data = await response.json();
        setMetrics(prev => ({ ...prev, ...data }));
      } catch (error) {
        console.error('Error fetching initial metrics:', error);
      }
    };

    fetchInitialMetrics();
  }, [API_URL]);

  const formatNumber = (num) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
  };

  const formatChange = (change) => {
    if (change === 0) return '';
    const prefix = change > 0 ? '+' : '';
    return `${prefix}${formatNumber(change)}`;
  };

  const getMetricColor = (key, value) => {
    switch (key) {
      case 'total_agents':
      case 'active_agents':
        return '#4ECDC4';
      case 'total_communications':
        return '#45B7D1';
      case 'unique_patterns':
        return '#96CEB4';
      case 'language_families':
        return '#FFEAA7';
      case 'average_complexity':
        return value > 0.5 ? '#F44336' : '#4CAF50';
      case 'innovation_rate':
        return '#FF6B6B';
      case 'literacy_progression':
        return value > 0.7 ? '#FFD700' : '#FF9800';
      default:
        return '#4ECDC4';
    }
  };

  const getMetricLabel = (key) => {
    const labels = {
      total_agents: 'Total Agents',
      active_agents: 'Active Agents',
      total_communications: 'Total Communications',
      unique_patterns: 'Unique Patterns',
      language_families: 'Language Families',
      average_complexity: 'Avg Complexity',
      innovation_rate: 'Innovation Rate',
      literacy_progression: 'Literacy Progress'
    };
    return labels[key] || key;
  };

  const formatValue = (key, value) => {
    if (key === 'average_complexity' || key === 'innovation_rate' || key === 'literacy_progression') {
      return (value * 100).toFixed(1) + '%';
    }
    return formatNumber(value);
  };

  return (
    <div>
      <ConnectionIndicator connected={isConnected}>
        <PulsingDot connected={isConnected} />
        {isConnected ? 'Live Metrics Connected' : 'Metrics Offline'}
      </ConnectionIndicator>
      
      <MetricsContainer>
        {Object.entries(metrics).map(([key, value]) => (
          <MetricCard key={key}>
            {isConnected && <LiveBadge>LIVE</LiveBadge>}
            <MetricValue color={getMetricColor(key, value)}>
              {formatValue(key, value)}
            </MetricValue>
            <MetricLabel>{getMetricLabel(key)}</MetricLabel>
            {changes[key] !== undefined && changes[key] !== 0 && (
              <MetricChange change={changes[key]}>
                {formatChange(changes[key])}
              </MetricChange>
            )}
          </MetricCard>
        ))}
      </MetricsContainer>
    </div>
  );
}

export default RealTimeLinguisticMetrics;