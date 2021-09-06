<img src="http://markdown-img-1304853431.cosgz.myqcloud.com/20210905104616.jpg" alt="8ac4643ca12c16394e1cc8ef1fa4504" style="zoom:50%;" />



# The 2048 Project

We try to use Artificial Intelligence, Machine Learning, and traditional algorithms to create a bot that out-performs human when playing 2048

# Benchmark

How to evaluate one game: *The sum of all numbers in the state when game is over*

Below data: Let each agent play 2,000 games and calculate the summary statistics from all scores.

|                         | Std.     | Med  | Mean    | Max  | Min  |
| ----------------------- | -------- | ---- | ------- | ---- | ---- |
| Greedy Agent            | 128.4185 | 256  | 227.232 | 1024 | 32   |
| Genetic Algorithm Agent | 132.7719 | 256  | 232.176 | 1024 | 32   |

# Agents Deployed

## Greedy Agent

Greedy Agent always choose the action that can merge most amount of tiles.

## Genetic Algorithm Agent

Genetic Algorithm agent will evaluate an action based on three factors

| Factor                   | Description                                                  |
| ------------------------ | ------------------------------------------------------------ |
| Empty Tile Number $w_1 $ | The number of empty tiles on                                 |
| Max Tile Number $w_2$    | The maximum number in the state                              |
| Action Preference $b_1$  | Agent's own preference to each action (up, down, left, right) |

$$
Evaluate(a, s) = w_1\cdot EmptyTile + w_2 \cdot MaxTile + b_1
$$

![image-20210905205351420](https://markdown-img-1304853431.cos.ap-guangzhou.myqcloud.com/image-20210905205351420.png)

## Tree Evaluate Agent

Tree Evaluate Agent use a function `tree_evaluation` to evaluate each action.

```python
def tree_evaluation(
        state: List[List],
        evaluate_fn,
        comb_fn,
        depth: int,
        sampling: Tuple[bool, int] = (False, 0),
        useMultiProcess: bool = False,
        gameOverScore: float = 0):
```

The process of tree_evaluation can be described in four parts:

* Sampling - Creating possible states for each action. There are two types of sampling - enumerate and random. The detail will be described in later section.
* Evaluating - If depth reach 0, Evaluate leaf state using given parameter `evaluate_fn`.
* Combine - Combine all evaluations to possible states using function `comb_fn`, then record the combined score as score of action.
* Maximize - For each state, return the *max* score of all 4 actions as the score of this state.

![image-20210905211155475](https://markdown-img-1304853431.cos.ap-guangzhou.myqcloud.com/image-20210905211155475.png)

### Sampling

There are two types of sampling - `random` and `deterministic`. 

When using `random` sampling, the first value of `sampling` will be `True`. In this case, function will create `n` amount of possible state by random generating tiles for `n` times (`n` is the value second element of `sampling` parameter).

When using `determinstic` sampling, first value of sampling will be `false`.In this case, the function will enumerate all possible states.

