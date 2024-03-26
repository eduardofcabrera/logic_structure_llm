

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b d)
(on c b)
(ontable d)
(ontable e)
(clear a)
(clear e)
)
(:goal
(and
(on c d)
(on d a)
(on e c))
)
)


