

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(on c b)
(ontable d)
(on e d)
(clear a)
(clear c)
(clear e)
)
(:goal
(and
(on a c)
(on d e))
)
)


