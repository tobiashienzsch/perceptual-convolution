#include <cstdint>
#include <cstdio>
#include <map>
#include <optional>

struct NonUniformPartitionOptimizer {
  struct State {
    int N{0};
    int S{0};
    int Q{0};
    double cost{0.0};
  };

  NonUniformPartitionOptimizer(int block_size, int filter_size)
      : _block_size{block_size}, _filter_size{filter_size},
        _num_blocks{(filter_size + block_size - 1) / block_size} {}

  auto operator()() -> State {
    auto const best = recurse(State{1, 1, 1, transition_cost(1)}, 1);
    backtrack(best, _num_blocks);
    return best;
  }

  std::uint64_t invocations{0};

private:
  auto recurse(State current, int block_index) -> State {
    ++invocations;

    if (block_index > _num_blocks) {

      return current;
    }

    // 1. Continuation
    auto best = std::optional<State>{};
    if (current.Q < current.S) {
      auto next = current;
      next.Q += 1;
      best = recurse(next, block_index + 1);
    }

    // 2. Repetition
    if (current.S == current.Q) {
      auto next = current;
      next.N += next.S;
      next.Q = 1;
      next.cost += repetition_cost(current.S);
      auto foo = recurse(next, block_index + 1);
      if (not best or (foo.cost < best->cost)) {
        best = foo;
      }
    }

    // 3. Transition
    if (current.S == current.Q) {
      auto const y = current.S * 2;
      auto next = current;
      next.N += y;
      next.S = y;
      next.Q = 1;
      next.cost += transition_cost(y);
      auto causal = (next.N - next.S + 1) >= 0;
      if (causal and (next.S * _block_size <= 32768 * 1)) {
        auto foo = recurse(next, block_index + 1);
        if (not best or (foo.cost < best->cost)) {
          best = foo;
        }
      }
    }

    return best.value();
  }

  auto backtrack(State current, int block_index) -> void {
    if (block_index == 0) {
      return;
    }
    std::printf("%2dB (%2d, %2d, %2d) (%f)\n", block_index, current.N,
                current.S, current.Q, current.cost);

    if (current.Q == current.S) {
      auto prev = current;
      // prev.N -= 1;
      prev.Q -= 1;
      backtrack(prev, block_index - 1);
    }

    if (current.Q == 1) {
      auto const t = transition_cost(current.S / 2);
      auto const r = repetition_cost(current.S);
      std::printf("t: %f, r: %f\n", t, r);
      // auto prev = current;
      // prev.Q -= 1;
      // backtrack(prev, block_index - 1);
    }
  }

  auto transition_cost(int block_index) -> double {
    auto B = _block_size * block_index;
    auto B2 = 2 * B;
    auto cost = _fft.at(B2) + _mul.at(B + 1) + _fft.at(B2) + _add.at(B);
    return cost / static_cast<double>(B);
    return 0.0;
  }

  auto repetition_cost(int block_index) -> double {
    auto B = _block_size * block_index;
    return _mul.at(B + 1) / static_cast<double>(B);
    return 0.0;
  }

  int _block_size;
  int _filter_size;
  int _num_blocks;

  std::map<int, double> _fft{
      {128, 0.33},  {256, 0.677}, {512, 0.99},   {1024, 1.26},  {2048, 2.1},
      {4096, 4.91}, {8192, 9.92}, {16384, 20.4}, {32768, 55.0}, {65536, 97.0},
  };

  std::map<int, double> _mul{
      {128 + 1, 5},         {256 + 1, 10},
      {512 + 1, 21},        {1024 + 1, 45},
      {2048 + 1, 690.0},    {4096 + 1, 1504.0},
      {8192 + 1, 3022.0},   {16384 + 1, 6044.0},
      {32768 + 1, 12087.0}, {65536 + 1, 12087.0 * 2.0},
  };

  std::map<int, double> _add{
      {128, 5},         {256, 10},
      {512, 21},        {1024, 45},
      {2048, 690.0},    {4096, 1504.0},
      {8192, 3022.0},   {16384, 6044.0},
      {32768, 12087.0}, {65536, 12087.0 * 2},
  };
};

auto main() -> int {
  auto optimizer = NonUniformPartitionOptimizer{128, 1024 * 30};
  auto state = optimizer();
  std::printf("----\n    (%2d, %2d, %2d) (%f)\n", state.N, state.S, state.Q,
              state.cost);
  std::printf("%lu\n", optimizer.invocations);
  return 0;
}
