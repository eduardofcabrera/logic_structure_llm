

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(ontable c)
(on d c)
(on e d)
(clear a)
(clear e)
)
(:goal
(and
(on a c)
(on c b))
)
)


