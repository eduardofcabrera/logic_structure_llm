

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b c)
(ontable c)
(on d b)
(on e d)
(clear a)
)
(:goal
(and
(on b e)
(on c b)
(on e d))
)
)


