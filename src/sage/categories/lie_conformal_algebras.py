r"""
Lie Conformal Algebras

Let `R` be a commutative ring, a *super Lie conformal algebra*
[Kac1997]_ over `R`
(also known as a *vertex Lie algebra*) is an `R[T]` super module `L`
together with a `\mathbb{Z}/2\mathbb{Z}`-graded `R`-bilinear
operation (called the `\lambda`-bracket)
`L\otimes L \rightarrow L[\lambda]`
(polynomials in `\lambda` with
coefficients in `L`), `a \otimes b \mapsto [a_\lambda b]` satisfying

1. Sesquilinearity:

   .. MATH::

        [Ta_\lambda b] = - \lambda [a_\lambda b], \qquad [a_\lambda Tb] =
        (\lambda+ T) [a_\lambda b].

2. Skew-Symmetry:

   .. MATH::

        [a_\lambda b] = - (-1)^{p(a)p(b)} [b_{-\lambda - T} a],

   where `p(a)` is `0` if `a` is *even* and `1` if `a` is *odd*. The
   bracket in the RHS is computed as follows. First we evaluate
   `[b_\mu a]` with the formal parameter `\mu` to the *left*, then
   replace each appearance of the formal variable `\mu` by `-\lambda - T`.
   Finally apply `T` to the coefficients in `L`.

3. Jacobi identity:

   .. MATH::

       [a_\lambda [b_\mu c]] = [ [a_{\lambda + \mu} b]_\mu c] +
       (-1)^{p(a)p(b)} [b_\mu [a_\lambda c]],

   which is understood as an equality in `L[\lambda, \mu]`.

   `T` is usually called the *translation operation* or the *derivative*.
   For an element `a \in L` we will say that `Ta` is the *derivative of*
   `a`. We define the `n`-*th products* `a_{(n)} b` for `a,b \in L` by

   .. MATH::

        [a_\lambda b] = \sum_{n \geq 0} \frac{\lambda^n}{n!} a_{(n)} b.

   A Lie conformal algebra is called *H-Graded* [DSK2006]_ if there exists
   a decomposition `L = \oplus L_n` such that the
   `\lambda`-bracket becomes graded of degree `-1`, that is:

   .. MATH::

        a_{(n)} b \in L_{p + q -n -1} \qquad
        a \in L_p, \: b \in L_q, \: n \geq 0.

   In particular this implies that the action of `T` increases
   degree by `1`.

.. NOTE::

    In the literature arbitrary gradings are allowed. In this
    implementation we only support non-negative rational gradings.


EXAMPLES:

1. The **Virasoro** Lie conformal algebra `Vir` over a ring `R`
   where `12` is invertible has two generators `L, C` as an `R[T]`-module.
   It is the direct sum of a free module of rank `1` generated by `L`, and
   a free rank one `R` module generated by `C` satisfying `TC = 0`.  `C`
   is central (the `\lambda`-bracket of `C` with any other vector
   vanishes). The remaining `\lambda`-bracket is given by

   .. MATH::

        [L_\lambda L] = T L + 2 \lambda L + \frac{\lambda^3}{12} C.

2. The **affine** or current Lie conformal algebra `L(\mathfrak{g})`
   associated to a finite dimensional Lie algebra `\mathfrak{g}` with
   non-degenerate, invariant `R`-bilinear form `(,)` is given as a central
   extension of the free
   `R[T]` module generated by `\mathfrak{g}` by a central element `K`. The
   `\lambda`-bracket of generators is given by

   .. MATH::

        [a_\lambda b] = [a,b] + \lambda (a,b) K, \qquad a,b \in \mathfrak{g}

3. The **Weyl** Lie conformal algebra, or `\beta-\gamma` system is
   given as the central extension of a free `R[T]` module with two
   generators `\beta` and `\gamma`, by a central element `K`.
   The only non-trivial brackets among generators are

   .. MATH::

        [\beta_\lambda \gamma] = - [\gamma_\lambda \beta] = K

4. The **Neveu-Schwarz** super Lie conformal algebra is a super Lie
   conformal algebra which is an extension of the Virasoro Lie conformal
   algebra. It consists of a Virasoro generator `L` as in example 1 above
   and an *odd* generator `G`. The remaining brackets are given by:

   .. MATH::

        [L_\lambda G] = \left( T + \frac{3}{2} \lambda \right) G \qquad
        [G_\lambda G] = 2 L + \frac{\lambda^2}{3} C

.. SEEALSO::

    - :mod:`sage.algebras.lie_conformal_algebras.lie_conformal_algebra`
    - :mod:`sage.algebras.lie_conformal_algebras.examples`

AUTHORS:

- Reimundo Heluani (2019-10-05): Initial implementation.
"""

#******************************************************************************
#       Copyright (C) 2019 Reimundo Heluani <heluani@potuz.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.categories.modules import Modules
from .category_types import Category_over_base_ring
from sage.misc.abstract_method import abstract_method
from sage.misc.cachefunc import cached_method
from sage.categories.graded_modules import GradedModulesCategory
from sage.categories.super_modules import SuperModulesCategory
from sage.categories.commutative_rings import CommutativeRings
from sage.misc.lazy_import import LazyImport

_CommutativeRings = CommutativeRings()

class LieConformalAlgebras(Category_over_base_ring):
    r"""
    The category of Lie conformal algebras.

    This is the base category for all Lie conformal algebras.
    Subcategories with axioms are ``FinitelyGenerated`` and
    ``WithBasis``. A *finitely generated* Lie conformal algebra is a
    Lie conformal algebra over `R` which is finitely generated as an
    `R[T]`-module. A Lie conformal algebra *with basis* is one with a
    preferred basis as an `R`-module.

    EXAMPLES:

    The base category::

        sage: C = LieConformalAlgebras(QQ); C
        Category of Lie conformal algebras over Rational Field
        sage: C.is_subcategory(VectorSpaces(QQ))
        True

    Some subcategories::

        sage: LieConformalAlgebras(QQbar).FinitelyGenerated().WithBasis()
        Category of finitely generated Lie conformal algebras with basis over Algebraic Field

    In addition we support functorial constructions ``Graded`` and
    ``Super``. These functors commute::

        sage: LieConformalAlgebras(AA).Graded().Super()
        Category of H-graded super Lie conformal algebras over Algebraic Real Field
        sage: LieConformalAlgebras(AA).Graded().Super() is LieConformalAlgebras(AA).Super().Graded()
        True

    That is, we only consider gradings on super Lie conformal algebras
    that are compatible with the `\ZZ/2\ZZ` grading.

    The base ring needs to be a commutative ring::

        sage: LieConformalAlgebras(QuaternionAlgebra(2))
        Traceback (most recent call last):
        ValueError: base must be a commutative ring got Quaternion Algebra (-1, -1) with base ring Rational Field
    """

    @staticmethod
    def __classcall_private__(cls, R, check=True):
        r"""
        INPUT:

        - `R` -- a commutative ring
        - ``check`` -- a boolean (default: ``True``); whether to check
          that `R` is a commutative ring

        EXAMPLES::

            sage: LieConformalAlgebras(QuaternionAlgebra(2))
            Traceback (most recent call last):
            ValueError: base must be a commutative ring got Quaternion Algebra (-1, -1) with base ring Rational Field
            sage: LieConformalAlgebras(ZZ)
            Category of Lie conformal algebras over Integer Ring
        """
        if check:
            if not (R in _CommutativeRings):
                    raise ValueError("base must be a commutative ring got {}".format(R))
        return super(LieConformalAlgebras,cls).__classcall__(cls,R)

    @cached_method
    def super_categories(self):
        """
        The list of super categories of this category.

        EXAMPLES::

            sage: C = LieConformalAlgebras(QQ)
            sage: C.super_categories()
            [Category of vector spaces over Rational Field]
            sage: C = LieConformalAlgebras(QQ).FinitelyGenerated(); C
            Category of finitely generated Lie conformal algebras over Rational Field
            sage: C.super_categories()
            [Category of Lie conformal algebras over Rational Field]
            sage: C.all_super_categories()
            [Category of finitely generated Lie conformal algebras over Rational Field,
             Category of Lie conformal algebras over Rational Field,
             Category of vector spaces over Rational Field,
             Category of modules over Rational Field,
             Category of bimodules over Rational Field on the left and Rational Field on the right,
             Category of right modules over Rational Field,
             Category of left modules over Rational Field,
             Category of commutative additive groups,
             Category of additive groups,
             Category of additive inverse additive unital additive magmas,
             Category of commutative additive monoids,
             Category of additive monoids,
             Category of additive unital additive magmas,
             Category of commutative additive semigroups,
             Category of additive commutative additive magmas,
             Category of additive semigroups,
             Category of additive magmas,
             Category of sets,
             Category of sets with partial maps,
             Category of objects]
        """
        return [Modules(self.base_ring())]

    def example(self):
        """
        An example of parent in this category.

        EXAMPLES::

            sage: LieConformalAlgebras(QQ).example()
            The Virasoro Lie conformal algebra over Rational Field
        """
        from sage.algebras.lie_conformal_algebras.virasoro_lie_conformal_algebra\
                                            import VirasoroLieConformalAlgebra
        return VirasoroLieConformalAlgebra(self.base_ring())

    def _repr_object_names(self):
        """
        The name of the objects of this category.

        EXAMPLES::

            sage: LieConformalAlgebras(QQ)
            Category of Lie conformal algebras over Rational Field
        """
        return "Lie conformal algebras over {}".format(self.base_ring())

    class ParentMethods:

        def is_super(self):
            """
            Wether this Lie conformal algebra is a super Lie
            conformal algebra.

            EXAMPLES::

                sage: V = lie_conformal_algebras.Virasoro(QQ)
                sage: V.is_super()
                False
                sage: lie_conformal_algebras.NeveuSchwarz(QQbar).is_super()
                True

            Notice that we can force to have a *purely even* super Lie
            conformal algebra::

                sage: bosondict = {('a','a'):{1:{('K',0):1}}}
                sage: R = LieConformalAlgebra(QQ,bosondict,names=('a',),
                ....:                         central_elements=('K',),super=True)
                sage: R.is_super()
                True
                sage: [g.is_even_odd() for g in R.gens()]
                [0, 0]
            """
            return self in LieConformalAlgebras(self.base_ring()).Super()

        def is_graded(self):
            """
            Wether this Lie conformal algebra is graded or not.

            EXAMPLES::

                sage: Vir = lie_conformal_algebras.Virasoro(QQ)
                sage: Vir
                The Virasoro Lie conformal algebra over Rational Field
                sage: Vir.is_graded()
                True
            """
            return self in LieConformalAlgebras(self.base_ring()).Graded()

        def is_with_basis(self):
            """
            Whether this Lie conformal algebra has a preferred basis.

            EXAMPLES::

                sage: Vir = lie_conformal_algebras.Virasoro(QQ)
                sage: Vir.is_with_basis()
                True
            """
            return self in LieConformalAlgebras(self.base_ring()).WithBasis()

        def is_finitely_generated(self):
            """
            Whether this Lie conformal algebra is finitely generated.

            EXAMPLES::

                sage: Vir = lie_conformal_algebras.Virasoro(QQ)
                sage: Vir.is_finitely_generated()
                True
            """
            return self in LieConformalAlgebras(self.base_ring()).FinitelyGenerated()

        def _test_jacobi(self, **options):
            """
            Test the Jacobi axiom of this Lie conformal algebra.

            INPUT:

            - ``options`` -- any keyword arguments acceptde by :meth:`_tester`

            EXAMPLES:

            By default, this method tests only the elements returned by
            ``self.some_elements()``::

                sage: V = lie_conformal_algebras.Affine(QQ, 'B2')
                sage: V._test_jacobi()      # long time (6 seconds)

            It works for super Lie conformal algebras too::

                sage: V = lie_conformal_algebras.NeveuSchwarz(QQ)
                sage: V._test_jacobi()

            We can use specific elements by passing the ``elements``
            keyword argument::

                sage: V = lie_conformal_algebras.Affine(QQ, 'A1', names=('e', 'h', 'f'))
                sage: V.inject_variables()
                Defining e, h, f, K
                sage: V._test_jacobi(elements=(e, 2*f+h, 3*h))

            TESTS::

                sage: wrongdict = {('a', 'a'): {0: {('b', 0): 1}}, ('b', 'a'): {0: {('a', 0): 1}}}
                sage: V = LieConformalAlgebra(QQ, wrongdict, names=('a', 'b'), parity=(1, 0))
                sage: V._test_jacobi()
                Traceback (most recent call last):
                ...
                AssertionError: {(0, 0): -3*a} != {}
                - {(0, 0): -3*a}
                + {}
            """
            tester = self._tester(**options)
            S = tester.some_elements()
            from sage.misc.misc import some_tuples
            from sage.functions.other import binomial
            pz = tester._instance.zero()
            for x,y,z in some_tuples(S, 3, tester._max_runs):
                brxy = x.bracket(y)
                brxz = x.bracket(z)
                bryz = y.bracket(z)
                br1 = {k: x.bracket(v) for k,v in bryz.items()}
                br2 = {k: v.bracket(z) for k,v in brxy.items()}
                br3 = {k: y.bracket(v) for k,v in brxz.items()}
                jac1 = {(j,k): v for k in br1 for j,v in br1[k].items()}
                jac3 = {(k,j): v for k in br3 for j,v in br3[k].items()}
                jac2 = {}
                for k,br in br2.items():
                    for j,v in br.items():
                        for r in range(j+1):
                            jac2[(k+r, j-r)] = jac2.get((k+r, j-r), pz)\
                                              + binomial(k+r, r)*v
                for k,v in jac2.items():
                    jac1[k] = jac1.get(k, pz) - v
                for k,v in jac3.items():
                    jac1[k] = jac1.get(k, pz) - v
                jacobiator = {k: v for k,v in jac1.items() if v}
                tester.assertDictEqual(jacobiator, {})

    class ElementMethods:

        def is_even_odd(self):
            """
            Return ``0`` if this element is *even* and ``1`` if it is
            *odd*.

            .. NOTE::

                This method returns ``0`` by default since every Lie
                conformal algebra can be thought as a purely even Lie
                conformal algebra. In order to
                implement a super Lie conformal algebra, the user
                needs to implement this method.

            EXAMPLES::

                sage: R = lie_conformal_algebras.NeveuSchwarz(QQ);
                sage: R.inject_variables()
                Defining L, G, C
                sage: G.is_even_odd()
                1
            """
            return 0

    class SubcategoryMethods:

        def FinitelyGeneratedAsLieConformalAlgebra(self):
            """
            The category of finitely generated Lie conformal algebras.

            EXAMPLES::

                sage: LieConformalAlgebras(QQ).FinitelyGenerated()
                Category of finitely generated Lie conformal algebras over Rational Field
            """
            return self._with_axiom("FinitelyGeneratedAsLieConformalAlgebra")

        def FinitelyGenerated(self):
            """
            The category of finitely generated Lie conformal algebras.

            EXAMPLES::

                sage: LieConformalAlgebras(QQ).FinitelyGenerated()
                Category of finitely generated Lie conformal algebras over Rational Field
            """
            return self._with_axiom("FinitelyGeneratedAsLieConformalAlgebra")

    class Super(SuperModulesCategory):
        """
        The category of super Lie conformal algebras.

        EXAMPLES::

            sage: LieConformalAlgebras(AA).Super()
            Category of super Lie conformal algebras over Algebraic Real Field
        """
        def example(self):
            """
            An example parent in this category.

            EXAMPLES::

                sage: LieConformalAlgebras(QQ).Super().example()
                The Neveu-Schwarz super Lie conformal algebra over Rational Field
            """
            from sage.algebras.lie_conformal_algebras.neveu_schwarz_lie_conformal_algebra\
                                          import NeveuSchwarzLieConformalAlgebra
            return NeveuSchwarzLieConformalAlgebra(self.base_ring())

        class ParentMethods:

            def is_super(self):
                """
                This method returns ``True``.

                EXAMPLES::

                    sage: V = lie_conformal_algebras.Virasoro(QQ)
                    sage: V.is_super()
                    False
                    sage: lie_conformal_algebras.NeveuSchwarz(QQbar).is_super()
                    True

                Notice that we can force to have a *purely even* super Lie
                conformal algebra::

                    sage: bosondict = {('a','a'):{1:{('K',0):1}}}
                    sage: R = LieConformalAlgebra(QQ,bosondict,names=('a',),
                    ....:                         central_elements=('K',),super=True)
                    sage: R.is_super()
                    True
                    sage: [g.is_even_odd() for g in R.gens()]
                    [0, 0]
                """
                return True

            def is_graded(self):
                """
                Wether this super Lie conformal algebra is graded or not.

                EXAMPLES::

                    sage: V = lie_conformal_algebras.NeveuSchwarz(QQ)
                    sage: V
                    The Neveu-Schwarz super Lie conformal algebra over Rational Field
                    sage: V.is_graded()
                    True
                """
                return self in LieConformalAlgebras(self.base_ring()).Graded().Super()

            def is_with_basis(self):
                """
                Whether this super Lie conformal algebra has a preferred
                basis by homogeneous elements.

                EXAMPLES::

                    sage: V = lie_conformal_algebras.NeveuSchwarz(QQ)
                    sage: V.is_with_basis()
                    True
                """
                return self in LieConformalAlgebras(self.base_ring()).WithBasis().Super()

            def is_finitely_generated(self):
                """
                Whether this super Lie conformal algebra is finitely generated.

                EXAMPLES::

                    sage: V = lie_conformal_algebras.NeveuSchwarz(QQ)
                    sage: V.is_finitely_generated()
                    True
                """
                return self in LieConformalAlgebras(self.base_ring()).FinitelyGenerated().Super()

            def _test_jacobi(self, **options):
                """
                Test the Jacobi axiom of this super Lie conformal algebra.

                INPUT:

                - ``options`` -- any keyword arguments acceptde by :meth:`_tester`

                EXAMPLES:

                By default, this method tests only the elements returned by
                ``self.some_elements()``::

                    sage: V = lie_conformal_algebras.Affine(QQ, 'B2')
                    sage: V._test_jacobi()      # long time (6 seconds)

                It works for super Lie conformal algebras too::

                    sage: V = lie_conformal_algebras.NeveuSchwarz(QQ)
                    sage: V._test_jacobi()

                We can use specific elements by passing the ``elements``
                keyword argument::

                    sage: V = lie_conformal_algebras.Affine(QQ, 'A1', names=('e', 'h', 'f'))
                    sage: V.inject_variables()
                    Defining e, h, f, K
                    sage: V._test_jacobi(elements=(e, 2*f+h, 3*h))

                TESTS::

                    sage: wrongdict = {('a', 'a'): {0: {('b', 0): 1}}, ('b', 'a'): {0: {('a', 0): 1}}}
                    sage: V = LieConformalAlgebra(QQ, wrongdict, names=('a', 'b'), parity=(1, 0))
                    sage: V._test_jacobi()
                    Traceback (most recent call last):
                    ...
                    AssertionError: {(0, 0): -3*a} != {}
                    - {(0, 0): -3*a}
                    + {}
                """
                tester = self._tester(**options)
                S = tester.some_elements()
                #Try our best to avoid non-homogeneous elements
                elements = []
                for s in S:
                    try:
                        s.is_even_odd()
                    except ValueError:
                        if tester._instance.is_with_basis():
                            elements.extend([s.even_component(),s.odd_component()])
                            continue
                    elements.append(s)
                S = elements
                from sage.misc.misc import some_tuples
                from sage.functions.other import binomial
                pz = tester._instance.zero()
                for x,y,z in some_tuples(S, 3, tester._max_runs):
                    if x.is_even_odd()*y.is_even_odd():
                        sgn = -1
                    else:
                        sgn = 1
                    brxy = x.bracket(y)
                    brxz = x.bracket(z)
                    bryz = y.bracket(z)
                    br1 = {k: x.bracket(v) for k,v in bryz.items()}
                    br2 = {k: v.bracket(z) for k,v in brxy.items()}
                    br3 = {k: y.bracket(v) for k,v in brxz.items()}
                    jac1 = {(j,k): v for k in br1 for j,v in br1[k].items()}
                    jac3 = {(k,j): v for k in br3 for j,v in br3[k].items()}
                    jac2 = {}
                    for k,br in br2.items():
                        for j,v in br.items():
                            for r in range(j+1):
                                jac2[(k+r, j-r)] = jac2.get((k+r, j-r), pz)\
                                                  + binomial(k+r, r)*v
                    for k,v in jac2.items():
                        jac1[k] = jac1.get(k, pz) - v
                    for k,v in jac3.items():
                        jac1[k] = jac1.get(k, pz) - sgn*v
                    jacobiator = {k: v for k,v in jac1.items() if v}
                    tester.assertDictEqual(jacobiator, {})

        class ElementMethods:

            @abstract_method
            def is_even_odd(self):
                """
                Return ``0`` if this element is *even* and ``1`` if it is
                *odd*.

                EXAMPLES::

                    sage: R = lie_conformal_algebras.NeveuSchwarz(QQ);
                    sage: R.inject_variables()
                    Defining L, G, C
                    sage: G.is_even_odd()
                    1
                """

        class Graded(GradedModulesCategory):
            """
            The subcategory of H-graded super Lie conformal algebras.

            EXAMPLES::

                sage: C = LieConformalAlgebras(QQbar)
                sage: C.Graded().Super()
                Category of H-graded super Lie conformal algebras over Algebraic Field
                sage: C.Graded().Super() is C.Super().Graded()
                True
            """
            def _repr_object_names(self):
                """
                The names of the objects of this category

                EXAMPLES::

                    sage: LieConformalAlgebras(QQbar).Graded()
                    Category of H-graded Lie conformal algebras over Algebraic Field
                """
                return "H-graded {}".format(self.base_category().\
                                            _repr_object_names())

    class Graded(GradedModulesCategory):
        """
        The subcategory of H-graded Lie conformal algebras.

        EXAMPLES::

            sage: LieConformalAlgebras(QQbar).Graded()
            Category of H-graded Lie conformal algebras over Algebraic Field
        """
        def _repr_object_names(self):
            """
            The names of the objects of this category

            EXAMPLES::

                sage: LieConformalAlgebras(QQbar).Graded()
                Category of H-graded Lie conformal algebras over Algebraic Field
            """
            return "H-graded {}".format(self.base_category().\
                                        _repr_object_names())

        class SubcategoryMethods:
            def Super(self, base_ring=None):
                """
                The category of H-graded super Lie conformal algebras.

                EXAMPLES::

                    sage: LieConformalAlgebras(QQ).Super().Graded()
                    Category of H-graded super Lie conformal algebras over Rational Field
                """
                assert base_ring is None or base_ring is self.base_ring()
                return SuperModulesCategory.category_of(
                                         self.base_category()).Graded()

    WithBasis = LazyImport('sage.categories.lie_conformal_algebras_with_basis',
                           'LieConformalAlgebrasWithBasis')

    FinitelyGeneratedAsLieConformalAlgebra = LazyImport(
        'sage.categories.finitely_generated_lie_conformal_algebras',
        'FinitelyGeneratedAsLieConformalAlgebra')
