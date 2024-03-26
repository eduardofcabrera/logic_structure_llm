

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(on b a)
(on c b)
(ontable d)
(on e d)
(clear c)
)
(:goal
(and
(on a b)
(on d c)
(on e d))
)
)


