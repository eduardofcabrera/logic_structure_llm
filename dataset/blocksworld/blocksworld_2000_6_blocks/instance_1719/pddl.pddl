

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b a)
(on c b)
(ontable d)
(on e c)
(clear d)
(clear e)
)
(:goal
(and
(on a b)
(on b c)
(on d a)
(on e d))
)
)

