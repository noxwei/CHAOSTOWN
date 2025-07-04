import { useEffect, useRef, useState } from 'react';

const useWebSocket = (url, options = {}) => {
  const {
    onMessage,
    onOpen,
    onClose,
    onError,
    reconnectAttempts = 5,
    reconnectInterval = 5000,
    protocols = []
  } = options;

  const [readyState, setReadyState] = useState(WebSocket.CONNECTING);
  const [lastMessage, setLastMessage] = useState(null);
  const [connectionAttempts, setConnectionAttempts] = useState(0);
  
  const websocket = useRef(null);
  const reconnectTimeoutId = useRef(null);
  const shouldReconnect = useRef(true);

  const connect = () => {
    if (connectionAttempts >= reconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    try {
      websocket.current = new WebSocket(url, protocols);
      
      websocket.current.addEventListener('open', (event) => {
        setReadyState(WebSocket.OPEN);
        setConnectionAttempts(0);
        console.log(`WebSocket connected to ${url}`);
        onOpen?.(event);
      });

      websocket.current.addEventListener('message', (event) => {
        try {
          const data = JSON.parse(event.data);
          setLastMessage(data);
          onMessage?.(data, event);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      });

      websocket.current.addEventListener('close', (event) => {
        setReadyState(WebSocket.CLOSED);
        console.log(`WebSocket disconnected from ${url}`);
        onClose?.(event);
        
        if (shouldReconnect.current && connectionAttempts < reconnectAttempts) {
          setConnectionAttempts(prev => prev + 1);
          reconnectTimeoutId.current = setTimeout(() => {
            connect();
          }, reconnectInterval);
        }
      });

      websocket.current.addEventListener('error', (event) => {
        setReadyState(WebSocket.CLOSED);
        console.error(`WebSocket error on ${url}:`, event);
        onError?.(event);
      });

    } catch (error) {
      console.error('Error creating WebSocket:', error);
      setReadyState(WebSocket.CLOSED);
    }
  };

  const disconnect = () => {
    shouldReconnect.current = false;
    if (reconnectTimeoutId.current) {
      clearTimeout(reconnectTimeoutId.current);
    }
    if (websocket.current) {
      websocket.current.close();
    }
  };

  const sendMessage = (message) => {
    if (websocket.current && readyState === WebSocket.OPEN) {
      try {
        const messageString = typeof message === 'string' ? message : JSON.stringify(message);
        websocket.current.send(messageString);
        return true;
      } catch (error) {
        console.error('Error sending WebSocket message:', error);
        return false;
      }
    }
    return false;
  };

  useEffect(() => {
    connect();
    
    return () => {
      disconnect();
    };
  }, [url]);

  return {
    readyState,
    lastMessage,
    sendMessage,
    connectionAttempts,
    isConnected: readyState === WebSocket.OPEN,
    isConnecting: readyState === WebSocket.CONNECTING,
    disconnect
  };
};

export default useWebSocket;