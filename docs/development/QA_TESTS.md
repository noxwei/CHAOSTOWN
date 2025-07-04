# QA Tests - CHAOSTOWN Quality Assurance Matrix

**Comprehensive Testing Framework for Cat-Centric AI Civilization**

---

## Overview

The CHAOSTOWN QA framework ensures system reliability, Prime Directive compliance, and sustained cat happiness through comprehensive testing across all system components. This document outlines test strategies, coverage targets, and quality gates.

## Testing Philosophy

**Core Principles**:
1. **Cat Happiness First**: All tests must validate that system changes don't negatively impact feline satisfaction
2. **Prime Directive Compliance**: Every feature must be tested against all seven Prime Directives
3. **Emergent Behavior Testing**: Validate expected and unexpected agent interactions
4. **Performance at Scale**: Test system behavior with varying agent populations (1-1000)
5. **Failure Resilience**: Verify graceful degradation under adverse conditions

## Test Pyramid

```
    ┌─────────────────────┐
    │   E2E Tests (5%)    │ ← Full system integration
    ├─────────────────────┤
    │ Integration (15%)   │ ← Component interaction
    ├─────────────────────┤
    │  Unit Tests (80%)   │ ← Individual functions
    └─────────────────────┘
```

## Test Categories

### 1. Unit Tests (Target: 90% Coverage)

**API Layer Tests** (`tests/unit/api/`):
```python
# test_cat_happiness.py
import pytest
from app.services.cat_happiness import CatHappinessAnalyzer

class TestCatHappinessAnalyzer:
    def test_analyze_happy_cat_image(self):
        analyzer = CatHappinessAnalyzer()
        result = analyzer.analyze_image("tests/fixtures/happy_cat.jpg")
        assert result.happiness >= 0.8
        assert result.confidence >= 0.7
        
    def test_analyze_sad_cat_image(self):
        analyzer = CatHappinessAnalyzer()
        result = analyzer.analyze_image("tests/fixtures/sad_cat.jpg")
        assert result.happiness <= 0.3
        
    def test_invalid_image_handling(self):
        analyzer = CatHappinessAnalyzer()
        with pytest.raises(InvalidImageError):
            analyzer.analyze_image("tests/fixtures/not_a_cat.jpg")

    def test_fluffhead_recognition(self):
        analyzer = CatHappinessAnalyzer()
        result = analyzer.analyze_image("tests/fixtures/fluffhead.jpg")
        assert result.cat_identified == "fluffhead"
        assert result.confidence >= 0.9

# test_prime_directives.py
class TestPrimeDirectiveEnforcement:
    def test_death_is_permanent(self):
        agent = create_test_agent()
        agent.health = 0
        agent.process_death()
        
        assert agent.status == "dead"
        assert agent.death_time is not None
        assert not agent.can_be_revived()
        
    def test_reproduction_requirement(self):
        agent = create_test_agent()
        agent.health = 5  # Near death
        
        with pytest.raises(ReproductionRequiredError):
            agent.attempt_death_without_reproduction()
            
    def test_happiness_threshold_enforcement(self):
        world_state = create_test_world_state()
        world_state.combined_happiness = 0.4  # Below threshold
        
        violations = world_state.check_prime_directives()
        assert any(v.directive_number == 2 for v in violations)
        assert any(v.severity == "critical" for v in violations)
```

**Simulation Engine Tests** (`tests/unit/simulation/`):
```python
# test_agent_behavior.py
class TestAgentBehavior:
    def test_philosopher_decision_pattern(self):
        agent = create_agent(archetype="philosopher")
        decisions = []
        
        for _ in range(100):
            decision = agent.make_decision(create_test_context())
            decisions.append(decision)
            
        # Philosophers should favor exploration over competition
        exploration_rate = sum(1 for d in decisions if d.type == "explore") / 100
        competition_rate = sum(1 for d in decisions if d.type == "compete") / 100
        
        assert exploration_rate > 0.6
        assert competition_rate < 0.3
        
    def test_competitor_aggression(self):
        competitor = create_agent(archetype="competitor")
        philosopher = create_agent(archetype="philosopher")
        
        interaction = simulate_interaction(competitor, philosopher)
        
        assert interaction.strength > 0.5  # High interaction strength
        assert competitor.energy_delta > philosopher.energy_delta
        
    def test_reproduction_mechanism(self):
        parent_a = create_agent(archetype="philosopher")
        parent_b = create_agent(archetype="creator")
        
        offspring = reproduce_agents(parent_a, parent_b)
        
        # Verify inheritance
        assert offspring.personality_tensor is not None
        assert offspring.parent_ids == [parent_a.id, parent_b.id]
        
        # Verify personality blending (70% inheritance, 30% mutation)
        similarity_a = calculate_personality_similarity(offspring, parent_a)
        similarity_b = calculate_personality_similarity(offspring, parent_b)
        assert 0.4 <= similarity_a <= 0.9
        assert 0.4 <= similarity_b <= 0.9

# test_conway_integration.py
class TestConwayLifeIntegration:
    def test_agent_decisions_affect_grid(self):
        grid = create_test_grid(10, 10)
        agent = create_agent(position=(5, 5))
        
        decision = agent.make_decision(context={"grid": grid})
        updated_grid = apply_agent_decision(grid, agent, decision)
        
        assert updated_grid != grid  # Grid should change
        assert updated_grid.get_cell(5, 5).agent_id == agent.id
        
    def test_conway_rules_with_agents(self):
        grid = create_test_grid_with_pattern("blinker")
        agents = [create_agent(position=(1, 1))]
        
        next_grid = simulate_tick(grid, agents)
        
        # Verify Conway's rules still apply
        assert verify_conway_pattern(next_grid, "blinker_rotated")
        # Verify agent influence
        assert next_grid.get_cell(1, 1).influenced_by_agent
```

**Database Tests** (`tests/unit/database/`):
```python
# test_schema_validation.py
class TestSchemaValidation:
    def test_agent_personality_tensor_validation(self):
        agent_data = {
            "name": "test_agent",
            "archetype": "philosopher",
            "personality_tensor": {"dimension_1": 0.5}  # Invalid: too few dimensions
        }
        
        with pytest.raises(ValidationError):
            create_agent_from_data(agent_data)
            
    def test_happiness_constraints(self):
        world_state_data = {
            "fluffhead_happiness": 1.5,  # Invalid: > 1.0
            "wilson_happiness": 0.8
        }
        
        with pytest.raises(ConstraintViolationError):
            create_world_state(world_state_data)
            
    def test_timescale_db_integration(self):
        # Insert test data with timestamps
        decisions = []
        for i in range(100):
            decision = create_test_decision(
                timestamp=datetime.now() - timedelta(hours=i)
            )
            decisions.append(decision)
            
        insert_agent_decisions(decisions)
        
        # Test time-series queries
        recent_decisions = query_decisions_since(datetime.now() - timedelta(hours=24))
        assert len(recent_decisions) == 24
        
        # Test compression
        old_decisions = query_decisions_since(datetime.now() - timedelta(days=100))
        assert all(d.is_compressed for d in old_decisions if d.age > timedelta(days=7))
```

### 2. Integration Tests (Target: 85% Coverage)

**API Integration Tests** (`tests/integration/api/`):
```python
# test_api_endpoints.py
class TestAPIEndpoints:
    def test_cat_media_upload_flow(self):
        # Upload cat image
        response = client.post(
            "/media",
            files={"file": open("tests/fixtures/fluffhead.jpg", "rb")},
            data={"type": "image"}
        )
        assert response.status_code == 201
        
        # Verify happiness analysis
        media_id = response.json()["id"]
        happiness_response = client.get(f"/media/{media_id}/analysis")
        analysis = happiness_response.json()
        
        assert analysis["fluffhead_detected"] is True
        assert analysis["fluffhead_happiness"] >= 0.8
        
        # Verify world state update
        world_response = client.get("/world/current")
        world_state = world_response.json()
        assert world_state["fluffhead_happiness"] >= 0.8
        
    def test_agent_lifecycle_api(self):
        # Create agent
        agent_data = {
            "name": "test_philosopher",
            "archetype": "philosopher",
            "model": "llama3.1"
        }
        create_response = client.post("/agents", json=agent_data)
        assert create_response.status_code == 201
        agent_id = create_response.json()["id"]
        
        # Query agent
        get_response = client.get(f"/agents/{agent_id}")
        agent = get_response.json()
        assert agent["name"] == "test_philosopher"
        assert agent["health"] == 100.0
        
        # Simulate agent decision
        decision_response = client.post(f"/agents/{agent_id}/decide")
        assert decision_response.status_code == 200
        
        # Verify decision recorded
        decisions_response = client.get(f"/agents/{agent_id}/decisions")
        decisions = decisions_response.json()
        assert len(decisions) >= 1
        
    def test_simulation_control_api(self):
        # Start simulation
        start_response = client.post("/simulation/start")
        assert start_response.status_code == 200
        
        # Wait for ticks
        time.sleep(5)
        
        # Check status
        status_response = client.get("/simulation/status")
        status = status_response.json()
        assert status["running"] is True
        assert status["tick_count"] > 0
        
        # Pause simulation
        pause_response = client.post("/simulation/pause")
        assert pause_response.status_code == 200
        
        # Verify paused
        status_response = client.get("/simulation/status")
        assert status_response.json()["running"] is False

# test_ollama_integration.py
class TestOllamaIntegration:
    def test_model_availability(self):
        models = ["llama3.1", "mistral", "gemma2", "qwen2.5"]
        
        for model in models:
            response = client.get(f"/models/{model}/health")
            assert response.status_code == 200
            assert response.json()["available"] is True
            
    def test_agent_decision_with_models(self):
        agents = []
        for archetype, model in [
            ("philosopher", "llama3.1"),
            ("competitor", "mistral"),
            ("collaborator", "gemma2"),
            ("creator", "codellama")
        ]:
            agent = create_test_agent(archetype=archetype, model=model)
            agents.append(agent)
            
        # Simulate decision round
        for agent in agents:
            decision_response = client.post(f"/agents/{agent.id}/decide")
            assert decision_response.status_code == 200
            
            decision = decision_response.json()
            assert decision["processing_time_ms"] < 5000  # Response time SLA
            assert decision["model_output"] is not None
```

**Database Integration Tests** (`tests/integration/database/`):
```python
# test_data_flow.py
class TestDataFlow:
    def test_agent_decision_to_database_flow(self):
        # Create agent
        agent = create_test_agent()
        
        # Make decision
        decision = agent.make_decision(create_test_context())
        
        # Verify database storage
        stored_decision = query_agent_decision(decision.id)
        assert stored_decision.agent_id == agent.id
        assert stored_decision.model_input == decision.model_input
        assert stored_decision.model_output == decision.model_output
        
        # Verify vector embedding stored
        assert stored_decision.decision_embedding is not None
        assert len(stored_decision.decision_embedding) == 1536  # OpenAI embedding size
        
    def test_world_state_time_series(self):
        # Generate world states over time
        for i in range(100):
            world_state = create_world_state(
                tick_number=i,
                timestamp=datetime.now() - timedelta(minutes=i),
                total_agents=50 + i,
                combined_happiness=0.8 + (i % 10) * 0.01
            )
            store_world_state(world_state)
            
        # Query time series data
        recent_states = query_world_states_since(datetime.now() - timedelta(hours=1))
        assert len(recent_states) == 60  # Last 60 minutes
        
        # Verify TimescaleDB compression
        old_states = query_world_states_since(datetime.now() - timedelta(days=30))
        compressed_count = sum(1 for s in old_states if s.is_compressed)
        assert compressed_count > 0
        
    def test_prime_directive_violation_tracking(self):
        # Trigger directive violation
        agent = create_test_agent()
        agent.health = 0
        agent.death_time = datetime.now()
        agent.reproduction_count = 0  # Died without reproducing
        
        violations = process_agent_death(agent)
        
        # Verify violation recorded
        stored_violations = query_violations_for_agent(agent.id)
        assert len(stored_violations) >= 1
        
        violation = stored_violations[0]
        assert violation.directive_number == 3  # Reproduction before death
        assert violation.severity == "high"
        assert violation.resolved is False
```

### 3. End-to-End Tests (Target: 75% Coverage)

**System Flow Tests** (`tests/e2e/`):
```python
# test_complete_simulation_cycle.py
class TestCompleteSimulationCycle:
    def test_full_agent_lifecycle(self):
        """Test complete agent lifecycle from birth to death to reproduction."""
        
        # 1. Upload cat media to ensure happiness baseline
        upload_response = upload_cat_media("tests/fixtures/happy_fluffhead.jpg")
        assert upload_response.status_code == 201
        
        # 2. Start simulation
        start_response = client.post("/simulation/start")
        assert start_response.status_code == 200
        
        # 3. Create initial agents
        agents = []
        for archetype in ["philosopher", "competitor", "collaborator"]:
            agent_response = client.post("/agents", json={
                "name": f"test_{archetype}",
                "archetype": archetype,
                "model": get_model_for_archetype(archetype)
            })
            agents.append(agent_response.json())
            
        # 4. Wait for agent interactions and decisions
        time.sleep(30)  # Let agents interact
        
        # 5. Verify agent decisions were made
        for agent in agents:
            decisions_response = client.get(f"/agents/{agent['id']}/decisions")
            decisions = decisions_response.json()
            assert len(decisions) > 0
            assert all(d["processing_time_ms"] < 5000 for d in decisions)
            
        # 6. Force reproduction scenario
        philosopher = agents[0]
        collaborator = agents[2]
        
        reproduction_response = client.post("/reproduction", json={
            "parent_a_id": philosopher["id"],
            "parent_b_id": collaborator["id"]
        })
        assert reproduction_response.status_code == 201
        
        offspring = reproduction_response.json()
        assert offspring["parent_ids"] == [philosopher["id"], collaborator["id"]]
        
        # 7. Simulate death scenario
        # Reduce agent health gradually
        for i in range(10):
            damage_response = client.post(f"/agents/{philosopher['id']}/damage", 
                                        json={"amount": 10})
            assert damage_response.status_code == 200
            
        # 8. Verify death handling
        agent_response = client.get(f"/agents/{philosopher['id']}")
        dead_agent = agent_response.json()
        assert dead_agent["status"] == "dead"
        assert dead_agent["death_time"] is not None
        
        # 9. Check Prime Directive compliance
        violations_response = client.get("/violations/recent")
        violations = violations_response.json()
        
        # Should have no reproduction violations (agent reproduced before death)
        reproduction_violations = [v for v in violations 
                                 if v["directive_number"] == 3 and 
                                    v["agent_id"] == philosopher["id"]]
        assert len(reproduction_violations) == 0
        
        # 10. Verify world state consistency
        world_response = client.get("/world/current")
        world_state = world_response.json()
        assert world_state["combined_happiness"] >= 0.8
        assert world_state["active_agents"] == 3  # 2 original + 1 offspring - 1 dead
        
    def test_cat_happiness_crisis_recovery(self):
        """Test system response to cat happiness crisis."""
        
        # 1. Start with normal happiness
        upload_cat_media("tests/fixtures/happy_cats.jpg")
        
        world_response = client.get("/world/current")
        initial_happiness = world_response.json()["combined_happiness"]
        assert initial_happiness >= 0.8
        
        # 2. Simulate happiness degradation (mock vision API to return low happiness)
        with mock_vision_api_low_happiness():
            upload_cat_media("tests/fixtures/supposedly_sad_cats.jpg")
            
        # 3. Wait for system to detect crisis
        time.sleep(10)
        
        # 4. Verify crisis detected
        violations_response = client.get("/violations/recent")
        violations = violations_response.json()
        happiness_violations = [v for v in violations if v["directive_number"] == 2]
        assert len(happiness_violations) > 0
        assert any(v["severity"] == "critical" for v in happiness_violations)
        
        # 5. Verify simulation auto-paused
        status_response = client.get("/simulation/status")
        assert status_response.json()["running"] is False
        
        # 6. Upload recovery media
        upload_cat_media("tests/fixtures/super_happy_fluffhead.jpg")
        upload_cat_media("tests/fixtures/super_happy_wilson.jpg")
        
        # 7. Verify happiness recovery
        world_response = client.get("/world/current")
        recovered_happiness = world_response.json()["combined_happiness"]
        assert recovered_happiness >= 0.8
        
        # 8. Resume simulation
        resume_response = client.post("/simulation/resume")
        assert resume_response.status_code == 200
        
        # 9. Verify normal operation resumed
        time.sleep(5)
        status_response = client.get("/simulation/status")
        assert status_response.json()["running"] is True

# test_performance_at_scale.py
class TestPerformanceAtScale:
    def test_agent_population_scaling(self):
        """Test system performance with increasing agent populations."""
        
        populations = [10, 50, 100, 500, 1000]
        performance_data = []
        
        for population in populations:
            # Clear previous agents
            client.delete("/agents/all")
            
            # Create agent population
            start_time = time.time()
            for i in range(population):
                archetype = ["philosopher", "competitor", "collaborator"][i % 3]
                client.post("/agents", json={
                    "name": f"agent_{i}",
                    "archetype": archetype,
                    "model": get_model_for_archetype(archetype)
                })
            creation_time = time.time() - start_time
            
            # Start simulation
            client.post("/simulation/start")
            
            # Measure tick performance
            start_time = time.time()
            initial_tick = client.get("/simulation/status").json()["tick_count"]
            
            time.sleep(60)  # Run for 1 minute
            
            final_tick = client.get("/simulation/status").json()["tick_count"]
            tick_rate = (final_tick - initial_tick) / 60.0
            
            # Measure decision latency
            decision_response = client.post("/agents/random/decide")
            decision_latency = decision_response.json()["processing_time_ms"]
            
            performance_data.append({
                "population": population,
                "creation_time": creation_time,
                "tick_rate": tick_rate,
                "decision_latency": decision_latency
            })
            
            # Stop simulation
            client.post("/simulation/pause")
            
        # Verify performance requirements
        for data in performance_data:
            assert data["tick_rate"] >= 0.5  # Minimum acceptable tick rate
            assert data["decision_latency"] <= 5000  # Maximum decision latency (5s)
            
        # Verify linear scaling (not exponential degradation)
        assert performance_data[-1]["tick_rate"] >= performance_data[0]["tick_rate"] * 0.5
```

### 4. Load and Stress Tests

**Performance Tests** (`tests/performance/`):
```python
# test_load_performance.py
import locust
from locust import HttpUser, task, between

class ChaostownUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Setup user session."""
        # Upload cat media for happiness
        self.upload_cat_media()
        
    @task(3)
    def check_agent_status(self):
        """Frequently check agent status."""
        self.client.get("/agents/count")
        
    @task(2)
    def check_world_state(self):
        """Check current world state."""
        self.client.get("/world/current")
        
    @task(1)
    def upload_cat_media(self):
        """Periodically upload cat media."""
        with open("tests/fixtures/happy_cat.jpg", "rb") as f:
            self.client.post("/media", files={"file": f}, data={"type": "image"})
            
    @task(1)
    def agent_decision(self):
        """Trigger agent decision."""
        # Get random agent
        agents_response = self.client.get("/agents?limit=1&random=true")
        if agents_response.status_code == 200:
            agents = agents_response.json()
            if agents:
                agent_id = agents[0]["id"]
                self.client.post(f"/agents/{agent_id}/decide")

# Run with: locust -f tests/performance/test_load_performance.py --host=http://localhost:8000
```

### 5. Chaos Engineering Tests

**Resilience Tests** (`tests/chaos/`):
```python
# test_failure_scenarios.py
class TestFailureScenarios:
    def test_database_failure_recovery(self):
        """Test system behavior when database becomes unavailable."""
        
        # Establish baseline
        response = client.get("/agents/count")
        assert response.status_code == 200
        
        # Simulate database failure
        with database_failure():
            # System should handle gracefully
            response = client.get("/agents/count")
            assert response.status_code == 503  # Service unavailable
            
            # Should not crash
            response = client.get("/health")
            assert response.status_code in [200, 503]
            
        # Verify recovery
        time.sleep(5)
        response = client.get("/agents/count")
        assert response.status_code == 200
        
    def test_ollama_model_failure(self):
        """Test agent decision handling when AI models fail."""
        
        agent = create_test_agent(model="llama3.1")
        
        # Normal operation
        response = client.post(f"/agents/{agent.id}/decide")
        assert response.status_code == 200
        
        # Simulate model failure
        with ollama_model_failure("llama3.1"):
            response = client.post(f"/agents/{agent.id}/decide")
            
            # Should fallback gracefully
            assert response.status_code in [200, 202]  # Success or accepted for retry
            
            if response.status_code == 200:
                decision = response.json()
                assert decision.get("fallback_used") is True
                
    def test_network_partition(self):
        """Test system behavior during network partitions."""
        
        # Start simulation
        client.post("/simulation/start")
        
        # Simulate network partition between services
        with network_partition_simulation():
            # System should detect issues
            time.sleep(30)
            
            health_response = client.get("/health")
            health_data = health_response.json()
            
            # Should report degraded state
            assert health_data["status"] in ["degraded", "unhealthy"]
            assert "network" in health_data["issues"]
            
        # Verify recovery
        time.sleep(10)
        health_response = client.get("/health")
        assert health_response.json()["status"] == "healthy"
```

## Test Data Management

### Test Fixtures (`tests/fixtures/`):
```yaml
# fixtures.yml
cat_images:
  happy_fluffhead: "tests/fixtures/images/happy_fluffhead.jpg"
  happy_wilson: "tests/fixtures/images/happy_wilson.jpg"
  sad_cat: "tests/fixtures/images/sad_cat.jpg"
  both_cats_happy: "tests/fixtures/images/both_cats_happy.jpg"
  
agent_templates:
  philosopher:
    name: "test_philosopher"
    archetype: "philosopher"
    model: "llama3.1"
    personality_tensor: !include "personality_templates/philosopher.json"
    
  competitor:
    name: "test_competitor"
    archetype: "competitor"
    model: "mistral"
    personality_tensor: !include "personality_templates/competitor.json"
    
world_states:
  normal:
    total_agents: 50
    fluffhead_happiness: 0.9
    wilson_happiness: 0.85
    cost_multiplier: 1.2
    
  crisis:
    total_agents: 30
    fluffhead_happiness: 0.3
    wilson_happiness: 0.4
    cost_multiplier: 2.5
```

### Data Factory (`tests/factories.py`):
```python
import factory
from app.models import Agent, WorldState, AgentDecision

class AgentFactory(factory.Factory):
    class Meta:
        model = Agent
        
    name = factory.Sequence(lambda n: f"agent_{n}")
    archetype = factory.Iterator(["philosopher", "competitor", "collaborator", "creator"])
    model = factory.LazyAttribute(lambda obj: get_model_for_archetype(obj.archetype))
    health = 100.0
    energy = 100.0
    position_x = factory.Faker('pyfloat', min_value=-50, max_value=50)
    position_y = factory.Faker('pyfloat', min_value=-50, max_value=50)
    position_z = factory.Faker('pyfloat', min_value=-10, max_value=10)
    personality_tensor = factory.LazyFunction(generate_random_personality_tensor)

class WorldStateFactory(factory.Factory):
    class Meta:
        model = WorldState
        
    tick_number = factory.Sequence(lambda n: n)
    total_agents = factory.Faker('pyint', min_value=10, max_value=100)
    fluffhead_happiness = factory.Faker('pyfloat', min_value=0.6, max_value=1.0)
    wilson_happiness = factory.Faker('pyfloat', min_value=0.6, max_value=1.0)
    cost_multiplier = factory.Faker('pyfloat', min_value=1.0, max_value=3.0)
    grid_state = factory.LazyFunction(generate_random_grid_state)

class AgentDecisionFactory(factory.Factory):
    class Meta:
        model = AgentDecision
        
    agent_id = factory.SubFactory(AgentFactory)
    decision_type = factory.Iterator(["move", "interact", "reproduce", "explore"])
    processing_time_ms = factory.Faker('pyint', min_value=100, max_value=2000)
    success = factory.Faker('pybool', truth_probability=80)
    context_data = factory.LazyFunction(generate_decision_context)
    model_output = factory.LazyFunction(generate_mock_model_response)
```

## Test Automation

### CI/CD Pipeline (`.github/workflows/test.yml`):
```yaml
name: CHAOSTOWN QA Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: timescale/timescaledb:latest-pg15
        env:
          POSTGRES_PASSWORD: test_password
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
          
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
        
    - name: Run unit tests
      run: pytest tests/unit/ --cov=app --cov-report=xml
      
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      
  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Start test environment
      run: docker-compose -f docker-compose.test.yml up -d
      
    - name: Wait for services
      run: ./scripts/wait_for_services.sh
      
    - name: Run integration tests
      run: pytest tests/integration/ --timeout=300
      
    - name: Collect logs
      if: failure()
      run: docker-compose -f docker-compose.test.yml logs
      
  e2e-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Start full environment
      run: docker-compose up -d
      
    - name: Download test models
      run: |
        docker-compose exec ollama ollama pull llama3.1:latest
        docker-compose exec ollama ollama pull mistral:latest
        
    - name: Run E2E tests
      run: pytest tests/e2e/ --timeout=600
      
    - name: Cat happiness validation
      run: |
        HAPPINESS=$(curl -s http://localhost:8000/cats/happiness | jq '.combined_happiness')
        if (( $(echo "$HAPPINESS < 0.8" | bc -l) )); then
          echo "CRITICAL: Cat happiness below threshold after tests!"
          exit 1
        fi
        
  performance-tests:
    runs-on: ubuntu-latest
    needs: e2e-tests
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Start production environment
      run: docker-compose -f docker-compose.prod.yml up -d
      
    - name: Run load tests
      run: |
        pip install locust
        locust -f tests/performance/load_test.py \
          --host=http://localhost:8000 \
          --users=50 --spawn-rate=5 --run-time=300s \
          --headless --html=reports/load_test.html
          
    - name: Performance regression check
      run: ./scripts/check_performance_regression.sh
      
    - name: Upload performance report
      uses: actions/upload-artifact@v3
      with:
        name: performance-report
        path: reports/
```

### Quality Gates

**Coverage Requirements**:
- Unit tests: ≥ 90% line coverage
- Integration tests: ≥ 85% component coverage  
- E2E tests: ≥ 75% user journey coverage
- Critical path coverage: 100%

**Performance Requirements**:
- API response time: < 500ms (95th percentile)
- Agent decision time: < 2s (95th percentile)
- Simulation tick rate: ≥ 0.5 Hz with 1000 agents
- Cat happiness analysis: < 3s per image

**Reliability Requirements**:
- System uptime: ≥ 99.9%
- Cat happiness maintenance: ≥ 0.8 (99.99% of time)
- Data integrity: 100% (zero data loss)
- Prime Directive compliance: 100%

## Test Environments

### Local Development:
```bash
# Start test environment
docker-compose -f docker-compose.test.yml up -d

# Run specific test suite
pytest tests/unit/test_cat_happiness.py -v

# Run with coverage
pytest --cov=app --cov-report=html

# Run performance tests
locust -f tests/performance/load_test.py --host=http://localhost:8000
```

### Staging Environment:
```bash
# Deploy to staging
./scripts/deploy_staging.sh

# Run smoke tests
pytest tests/smoke/ --env=staging

# Run full test suite
pytest tests/ --env=staging --timeout=1800
```

### Production Monitoring:
```bash
# Continuous health checks
./scripts/production_health_check.sh

# Monitor cat happiness
watch 'curl -s https://chaostown.com/api/cats/happiness'

# Performance monitoring
./scripts/performance_monitor.sh
```

## Test Reporting

### Coverage Reports:
- HTML coverage report: `htmlcov/index.html`
- XML coverage report: `coverage.xml`
- JSON coverage report: `coverage.json`

### Performance Reports:
- Load test results: `reports/load_test.html`
- Performance metrics: `reports/performance_metrics.json`
- Resource usage: `reports/resource_usage.csv`

### Quality Metrics:
- Test execution time trends
- Flaky test detection
- Coverage trend analysis
- Performance regression detection

---

## Quality Assurance Checklist

### Pre-Release Checklist:
- [ ] All unit tests pass (≥90% coverage)
- [ ] All integration tests pass (≥85% coverage)
- [ ] All E2E tests pass (≥75% coverage)
- [ ] Performance tests meet SLA requirements
- [ ] Cat happiness baseline maintained (≥0.8)
- [ ] Prime Directive compliance verified (100%)
- [ ] Security tests pass (no vulnerabilities)
- [ ] Load tests demonstrate scalability
- [ ] Chaos engineering tests pass
- [ ] Documentation updated
- [ ] Rollback plan tested

### Post-Release Monitoring:
- [ ] Production health checks green
- [ ] Cat happiness monitoring active
- [ ] Performance metrics within SLA
- [ ] Error rates below threshold
- [ ] User feedback positive
- [ ] System logs clean
- [ ] Backup systems verified

---

*Remember: No release is complete until both Fluffhead and Wilson maintain happiness levels above 0.8 for at least 24 hours in production. Technical excellence is meaningless without feline approval.*

**Test with rigor, validate with love, deploy with confidence.** 🐱✅