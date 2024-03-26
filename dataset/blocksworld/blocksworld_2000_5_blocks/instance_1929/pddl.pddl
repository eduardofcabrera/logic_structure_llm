

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b d)
(on c b)
(ontable d)
(on e c)
(clear a)
(clear e)
)
(:goal
(and
(on d a))
)
)


