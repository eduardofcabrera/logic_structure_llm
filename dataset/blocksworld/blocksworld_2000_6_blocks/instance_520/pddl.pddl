

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(on b e)
(on c b)
(ontable d)
(on e d)
(clear a)
)
(:goal
(and
(on b a)
(on c b)
(on d e))
)
)


