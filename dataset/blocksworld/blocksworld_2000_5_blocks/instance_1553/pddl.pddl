

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b c)
(on c d)
(on d a)
(on e b)
(clear e)
)
(:goal
(and
(on a e)
(on e d))
)
)


