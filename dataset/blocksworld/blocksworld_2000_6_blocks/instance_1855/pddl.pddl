

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(ontable b)
(on c b)
(ontable d)
(on e c)
(clear a)
(clear e)
)
(:goal
(and
(on c a)
(on d e))
)
)


