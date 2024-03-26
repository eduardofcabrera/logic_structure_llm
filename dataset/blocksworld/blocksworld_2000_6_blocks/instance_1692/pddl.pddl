

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b e)
(on c b)
(on d a)
(on e d)
(clear c)
)
(:goal
(and
(on a b))
)
)


