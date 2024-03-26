

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(ontable b)
(ontable c)
(ontable d)
(on e d)
(clear a)
(clear b)
(clear e)
)
(:goal
(and
(on a c)
(on c b)
(on e a))
)
)


