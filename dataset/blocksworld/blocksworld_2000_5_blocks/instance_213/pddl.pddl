

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b a)
(on c e)
(ontable d)
(ontable e)
(clear b)
(clear d)
)
(:goal
(and
(on a b)
(on b d)
(on c a)
(on e c))
)
)


