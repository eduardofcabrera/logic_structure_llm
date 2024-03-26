

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(ontable b)
(on c d)
(ontable d)
(on e b)
(clear a)
(clear c)
)
(:goal
(and
(on a e)
(on c b)
(on d c))
)
)


