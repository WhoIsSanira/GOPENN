# GOPENN
Global Optical Potential Evaluator Neural-Network - open data-set neural network for systemizing and predicting the phenomenological optical potential parameters.

Optical potential is quite helpful, strong and, surprisingly, easy to understand phenomenologic model for describing nuclear matter.
Optical potential appears in Schrodinger equation:

$$ \frac{d^2 \Psi}{dr^2} + \frac{2 \mu}{\hbar^2} \left( E - V_{opt.}(r) \right) \Psi = 0 $$

$$V_{opt.}(r)$$ is defined as (without spin-orbit interaction):

$$V_{opt.}(r) = V_{R} * f(r, R_{V}, a_{V}) + iW_{V} * f(r, R_{W}, a_{W}) + 4ia_{S} W_{S} * \frac{d}{dr} f(r, R_{S}, a_{S})$$

where the $$f(r, R_{i}, a_{i})$$ is Woods-Saxon form factor

$$f(r, R_{i}, a_{i}) = \frac{1}{1 + exp \left( \frac{r - R_{i}}{a_{i}} \right)}$$

So, we have 9 different free parameters ($$V_{R}, W_{V}, W_{S}, R_{V}, R_{W}, R_{S}, a_{V}, a_{W}, a_{S}$$), that we need to fit to our experimental data.
It is so vast and diffucult to find out "good" parameters. These parameters must be physically meaningfull in one hand and in other hand must minimize the discrepancy between theory and experiment.
If you're not convinced yet, there are, so-called, discrete and continuous ambiguities of optical parameters, that makes the choice of them even worse.
Ambiguities state, that there are many set of parameters which can describe experimental data equally very well.

[Drisko, R. M., Satchler, G. R., & Bassel, R. H. (1963). Ambiguities in the optical potential for strongly absorbed projectiles. Physics Letters, 5(5).]

[Cage, M. E., Cole, A. J., & Pyle, G. J. (1973). Ambiguities and systematics in the real central part of the optical-model potential. Nuclear Physics A, 201(2), 418-432.]

For solving these problem, GOPENN fitting machine was build.
This NN takes as an input the target and projectile nuclei, the energy of proj. nucleus and outputs optimal optical model parameters. ~Honestly, we wish it will be able to do that~

<sup>Build by `WhoIsSanira` and `TheKoke`</sup>.

## Dataset
For early-beta version we considered only next range of nuclear reactions:
1. Target constraints &rarr; only `1 < A < 17`;
2. Projectile constraints &rarr;  p, d, <sup>3</sup>He, <sup>4</sup>He, <sup>6</sup>Li, <sup>7</sup>Li, <sup>8</sup>Li, <sup>9</sup>Be, <sup>10</sup>Be, <sup>10</sup>B, <sup>11</sup>B, <sup>12</sup>C, <sup>14</sup>N, <sup>15</sup>N, <sup>16</sup>O;
3. Energy constraints &rarr; $$1 \frac{MeV}{nucl.} < \frac{E}{A} < 10 \frac{MeV}{nucl.}$$;
4. Each dataset must contain "label" already known optimal OM parameters: $$V_{R}, W_{V}, W_{S}, R_{V}, R_{W}, R_{S}, a_{V}, a_{W}, a_{S}$$;
5. For each projectile nucleus there are 10 different reactions with arbitrary targets at arbitrary energies (with respect to our constraints). 15 projectiles &rarr; 150 datasets.
> Actually, we got only 145 labeled datasets caused by the lack of experimental data.