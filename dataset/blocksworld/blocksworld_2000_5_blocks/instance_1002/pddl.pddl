

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(on b c)
(on c a)
(ontable d)
(ontable e)
(clear b)
(clear e)
)
(:goal
(and
(on b e)
(on c a)
(on e c))
)
)


