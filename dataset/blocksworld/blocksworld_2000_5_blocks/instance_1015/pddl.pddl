

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(on c b)
(on d c)
(ontable e)
(clear d)
(clear e)
)
(:goal
(and
(on a b)
(on e c))
)
)


